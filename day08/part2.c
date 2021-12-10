#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>


#define NUM_PATTERNS 10
#define NUM_OUTPUTS 4


typedef char segments_t;


const static segments_t UNSET_SEGMENTS = 0b1111111;


#pragma clang diagnostic push
#pragma ide diagnostic ignored "OCUnusedGlobalDeclarationInspection"
void printSegments(const segments_t segments) {
    for (int i = 8; i > 0; i--) {
        if (((segments << i) & 0x80) != 0) {
            printf("%c", 'g' - i + 1);
        }
    }
    printf("\n");
}
#pragma clang diagnostic pop


int activeSegments(const segments_t segments) {
    int n = 0;
    for (int i = 0; i < 7; i++) {
        n += (segments >> i) & 1;
    }

    return n;
}


segments_t subtractSegments(const segments_t segments1, const segments_t segments2) {
    segments_t out = segments1;
    for (int i = 0; i < 8; i++) {
        // check if bit i is set
        if ((segments2 >> i) & 1) {
            // unset bit i
            out &= ~(1UL << i);
        }
    }
    return out;
}


typedef struct signal_node {
    segments_t patterns[10];
    segments_t outputs[4];
    struct signal_node *next;
} signal_node;


signal_node *createSignalNode(segments_t patterns[10], segments_t outputs[4]) {
    signal_node *signal_node = malloc(sizeof(struct signal_node));

    memcpy(signal_node->patterns, patterns, sizeof(signal_node->patterns));
    memcpy(signal_node->outputs, outputs, sizeof(signal_node->outputs));
    signal_node->next = NULL;

    return signal_node;
}


signal_node *parseSignal(FILE *file) {
    int c;

    segments_t segments = 0;
    segments_t patternsSegmentsList[NUM_PATTERNS] = {};
    segments_t outputsSegmentsList[NUM_OUTPUTS] = {};

    int i = 0;

    while ((c = fgetc(file)) != EOF) {
        if (c == ' ' || c == '\n') {
            if (i < 10) {
                patternsSegmentsList[i] = segments;
            } else {
                outputsSegmentsList[i - NUM_PATTERNS] = segments;
            }
            segments = 0;
            i++;
        } else if (c == '|') {
            fgetc(file); // skip next space
            continue;
        }
        if (c == '\n') {
            break;
        }
        // activate bit at position (c - 'a')
        segments |= 1 << (c - 'a');
    }

    if (i < 13) {
        return NULL;
    } else {
        return createSignalNode(patternsSegmentsList, outputsSegmentsList);
    }
}


segments_t findPattern(
    segments_t *searchArray,
    segments_t pattern,
    int shouldRemainActiveCount,
    bool subtractFromCandidate
) {
    segments_t out = -1;
    for (int i = 0; i < 3; i++) {
        if (searchArray[i] == UNSET_SEGMENTS) {
            continue;
        }

        segments_t tmp = subtractFromCandidate
            ? subtractSegments(searchArray[i], pattern)
            : subtractSegments(pattern, searchArray[i]);

        if (activeSegments(tmp) == shouldRemainActiveCount) {
            out = searchArray[i];
            searchArray[i] = UNSET_SEGMENTS;
            break;
        }
    }
    return out;
}


int compute(struct signal_node *signals) {
    struct signal_node *signalNode = signals;
    int n = 0;

    while (signalNode != NULL) {
        segments_t nums[10];

        segments_t fiveLenPatterns[3] = {0};
        int fiveLenPatIdx = 0;

        segments_t sixLenPatterns[3] = {0};
        int sixLenPatIdx = 0;

        int numSegments;
        for (int i = 0; i < NUM_PATTERNS; i++) {
            segments_t pattern = signalNode->patterns[i];
            numSegments = activeSegments(pattern);

            switch (numSegments) {
                case 2:
                    nums[1] = pattern;
                    break;
                case 3:
                    nums[7] = pattern;
                    break;
                case 4:
                    nums[4] = pattern;
                    break;
                case 7:
                    nums[8] = pattern;
                    break;
                case 5:
                    fiveLenPatterns[fiveLenPatIdx++] = pattern;
                    break;
                case 6:
                    sixLenPatterns[sixLenPatIdx++] = pattern;
                    break;
                default:
                    printf("Invalid segment count %d\n", numSegments);
                    exit(1);
            }
        }

        int i;

        nums[9] = findPattern(sixLenPatterns, nums[4], 2, true);
        nums[6] = findPattern(sixLenPatterns, nums[1], 1, false);
        for (i = 0; i < 3; i++) {
            if (sixLenPatterns[i] != UNSET_SEGMENTS) {
                nums[0] = sixLenPatterns[i];
            }
        }

        nums[5] = findPattern(fiveLenPatterns, nums[6], 1, false);
        nums[3] = findPattern(fiveLenPatterns, nums[9], 1, false);
        for (i = 0; i < 3; i++) {
            if (fiveLenPatterns[i] != UNSET_SEGMENTS) {
                nums[2] = fiveLenPatterns[i];
            }
        }

        for (i = 0; i < NUM_OUTPUTS; ++i) {
            int exp = NUM_OUTPUTS - i - 1;
            for (int j = 0; j < 10; ++j) {
                if (signalNode->outputs[i] == nums[j]) {
                    n += j * (int)pow(10, exp);
                    break;
                }
            }
        }
        signalNode = signalNode->next;
    }

    return n;
}


int main(void) {
    char filename[50];

    size_t slash_idx = strlen(__FILE__) - 1;

    while (__FILE__[slash_idx] != '\\')
        slash_idx--;

    strncpy(filename, __FILE__, slash_idx);
    strcat(filename, "\\input.txt");


    FILE *file = fopen(filename, "r");

    struct signal_node *signalHeadNode = parseSignal(file);
    struct signal_node *signalCurrNode = signalHeadNode;
    struct signal_node *newSignalNode = NULL;

    while ((newSignalNode = parseSignal(file)) != NULL) {
        signalCurrNode->next = newSignalNode;
        signalCurrNode = newSignalNode;
    }

    fclose(file);

    printf("%d", compute(signalHeadNode));

    return 0;
}
