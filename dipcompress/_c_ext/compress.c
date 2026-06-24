#include <stdint.h>
#include <string.h>

#define WINDOW_SIZE 4096
#define LOOKAHEAD   18

/*
 * lz77_encode — encodes `input_len` bytes into LZ77 token stream.
 *
 * Output format: each token is exactly 4 bytes:
 *   [distance_hi, distance_lo, length, next_byte]
 *
 * Literal tokens have distance=0 and length=0.
 * Back-references have distance>0 and length>=2.
 *
 * Returns: number of bytes written to `output` (always a multiple of 4).
 */
int lz77_encode(const uint8_t *input, int input_len,
                uint8_t *output, int output_max)
{
    int pos     = 0;
    int out_pos = 0;

    while (pos < input_len) {
        int window_start = pos - WINDOW_SIZE;
        if (window_start < 0) window_start = 0;

        int lookahead_end = pos + LOOKAHEAD;
        if (lookahead_end > input_len) lookahead_end = input_len;
        int lookahead_len = lookahead_end - pos;

        int best_distance = 0;
        int best_length   = 0;

        /* Scan every starting position in the window for the longest match. */
        for (int i = window_start; i < pos; i++) {
            int ml = 0;
            while (ml < lookahead_len &&
                   i + ml < pos &&
                   input[i + ml] == input[pos + ml]) {
                ml++;
            }
            if (ml > best_length) {
                best_length   = ml;
                best_distance = pos - i;
            }
        }

        if (best_length >= 3) {
            int next_pos = pos + best_length;
            /* Ensure next_pos always points to a valid byte. */
            if (next_pos >= input_len) {
                best_length--;
                next_pos--;
            }
            uint8_t next_byte = input[next_pos];

            output[out_pos++] = (best_distance >> 8) & 0xFF;
            output[out_pos++] =  best_distance       & 0xFF;
            output[out_pos++] = (uint8_t)best_length;
            output[out_pos++] = next_byte;

            pos += best_length + 1;
        } else {
            /* Literal token */
            output[out_pos++] = 0;
            output[out_pos++] = 0;
            output[out_pos++] = 0;
            output[out_pos++] = input[pos];
            pos++;
        }
    }

    return out_pos;
}
