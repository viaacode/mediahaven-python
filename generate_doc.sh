#!/bin/bash

handsdown
mv docs/README.md .
sed -i 's/mediahaven\//docs\/mediahaven\//g' README.md 