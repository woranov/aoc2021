#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>


#define NUM_PATTERNS 10
#define NUM_OUTPUTS 4


typedef bool segments_t[7];


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

    segments_t segments = {0};
    segments_t patternsSegmentsList[NUM_PATTERNS] = {};
    segments_t outputsSegmentsList[NUM_OUTPUTS] = {};

    int i = 0;

    while ((c = fgetc(file)) != EOF) {
        if (c == ' ' || c == '\n') {
            if (i < 10) {
                memcpy(patternsSegmentsList[i], segments, sizeof(patternsSegmentsList[i]));
            } else {
                memcpy(outputsSegmentsList[i - NUM_PATTERNS], segments, sizeof(outputsSegmentsList[i]));
            }
            memset(segments, 0, sizeof(segments));
            i++;
        } else if (c == '|') {
            fgetc(file); // skip next space
            continue;
        }
        if (c == '\n') {
            break;
        }
        segments[c - 'a'] = true;
    }

    if (i < 13) {
        return NULL;
    } else {
        return createSignalNode(patternsSegmentsList, outputsSegmentsList);
    }
}


int compute(struct signal_node *signals) {
    struct signal_node *signalNode = signals;
    int n = 0;

    while (signalNode != NULL) {
        for (int outputIdx = 0; outputIdx < NUM_OUTPUTS; outputIdx++) {
            int numSegments = 0;
            for (int i = 0; i < 7; i++) {
                numSegments += signalNode->outputs[outputIdx][i];
            }
            if (
                    numSegments == 2 ||
                    numSegments == 3 ||
                    numSegments == 4 ||
                    numSegments == 7
                    ) {
                n += 1;
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
