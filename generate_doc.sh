#!/bin/bash

handsdown
mv docs/README.md .
sed -i 's/mediahaven\//docs\/mediahaven\//g' README.md
find docs/ -type f -exec sed -i 's/\.\.\/README\.md/..\/..\/README.md/g' {} \;