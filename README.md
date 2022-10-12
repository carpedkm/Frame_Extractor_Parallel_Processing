# Frame_Extractor_Parallel_Processing

* step 1: Download raw videos

* step 2: Extract frames from raw videos

We use ffmpeg to extract frames from the video:

```
sudo apt-get update
sudo apt-get install ffmpeg
```

Install library for parallel processing
```
wget https://www.parallelpython.com/downloads/pp/pp-1.6.4.4.zip
unzip pp-1.6.4.4.zip && cd pp-1.6.4.4
python setup.py install && cd ..
```

## Usage
```
python parallel_frame_extract.py --source_dir [SOURCE DIRECTORY] --target_dir [TARGET DIRECTORY] --n_cpus [NUM OF CPUS]
```
