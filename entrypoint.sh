#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
repo_dir="$PWD"
weights="$repo_dir/resnet34_cerberus/weights.tar"
if [[ ! -r "$weights" || ! -s "$weights" ]]; then
    printf 'Mount a readable Cerberus weights.tar at %s\n' "$weights" >&2
    exit 1
fi

cerberus_rev=5bcecbb071bebd5911250034c94f3568f23f50bb
run_dir=$(mktemp -d)
trap 'rm -rf -- "$run_dir"' EXIT
checkout="$run_dir/cerberus"
git init -q "$checkout"
git -C "$checkout" fetch --depth 1 https://github.com/TissueImageAnalytics/cerberus.git "$cerberus_rev"
git -C "$checkout" checkout --detach "$cerberus_rev"
git -C "$checkout" apply "$repo_dir/for_cpu.patch"

cd "$checkout"
conda run --no-capture-output -n cerberus python run_infer_tile.py \
    --gpu="0" \
    --batch_size=25 \
    --model="$repo_dir/resnet34_cerberus" \
    --input_dir="$repo_dir/images_test/" \
    --output_dir="$run_dir/output/"

cd "$repo_dir"
for reference in output/test*.jpg; do
    conda run --no-capture-output -n cerberus python test.py \
        "$reference" "$run_dir/output/overlay/${reference##*/}"
done

mkdir -p output_test
cp -R "$run_dir/output/overlay" output_test/
