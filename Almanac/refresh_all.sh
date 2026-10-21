set -e
export PYTHONHASHSEED=0
cd "$(dirname "$0")"
python3 merge_albums.py > /dev/null
rm -rf out && python3 build.py > /dev/null
python3 post.py
python3 album_build.py && python3 albums.py && python3 album_finalize.py
python3 artist_albums.py
python3 life_build.py > /dev/null
python3 now_life_build.py > /dev/null
python3 metrics_build.py > /dev/null
python3 screams_build.py > /dev/null
python3 people_build.py > /dev/null
python3 emo_build.py > /dev/null
python3 solar_build.py > /dev/null
python3 lane_top_build.py > /dev/null
python3 recent_build.py > /dev/null
python3 bundle_build.py
echo built
