Require [docker](https://www.docker.com/products/docker-desktop/) with compose. (Docker Desktop contains compose functionality)

# Initial setting

Locate video files in `./video`, audio files in `./audio`. Then run the command below:

```
docker compose -f docker-compose-convert.yaml up
```

This command will convert video files to audio files to `./converted_video`.

# Running Test

The command below will generate result texts in `./results`. By default it takes up 80% of your cores.

```
docker compose -f docker-compose-run.yaml up
```

\* Options

In `docker-compose-run.yaml` file, the command looks like:
```
command: ["python", "main.py", "-m", "-th", "20", "-sr", "2048", "-mo", "2"]
```
- `th` : Video Matcher Threshold. Use GraphMatch Option(-mo 3) for tuning. model 3 draws graph.
- `sr` : Sampling rate for both videos and songs. Larger makes significantly slower but little more accurate
- `mo` : Video Matcher Mode. 1~4

# Example Result

console
```
PS F:\...> docker compose -f docker-compose-run.yaml up
[+] Running 1/1
 - Container ver2software-app-1  Recreated                                                                                                                                                                     1.4s 
Attaching to ver2software-app-1
ver2software-app-1  | Using 12 cores
ver2software-app-1  | Preprocessing, Feature Extraction Start for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3
ver2software-app-1  | ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 - shape: (84804608,), sr: 48000
ver2software-app-1  | ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 - resampled - shape: (3618330,), sr: 2048
ver2software-app-1  | Preprocessing, Feature Extraction for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 done with time: 37.02601957321167s
ver2software-app-1  | ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 already extracted, skipping...
ver2software-app-1  | Preprocessing, Feature Extraction Start for ./audio/오준성-04-Brand New-Day.mp3
ver2software-app-1  | ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 already extracted, skipping...
ver2software-app-1  | ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 already extracted, skipping...
ver2software-app-1  | ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 already extracted, skipping...
ver2software-app-1  | ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 already extracted, skipping...
ver2software-app-1  | ./audio/오준성-04-Brand New-Day.mp3 - shape: (4805615,), sr: 44100
ver2software-app-1  | ./audio/오준성-04-Brand New-Day.mp3 - resampled - shape: (223150,), sr: 2048
ver2software-app-1  | Preprocessing, Feature Extraction for ./audio/오준성-04-Brand New-Day.mp3 done with time: 1.8650009632110596s
ver2software-app-1  | Match process start for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-04-Brand New-Day.mp3
ver2software-app-1  | Matching Algorithm video shape: (7068, 32), audio shape: (436, 32)
ver2software-app-1  | Preprocessing, Feature Extraction Start for ./audio/오준성-09-Feel Good Soup.mp3
ver2software-app-1  | ./audio/오준성-09-Feel Good Soup.mp3 - shape: (4386287,), sr: 44100
ver2software-app-1  | ./audio/오준성-09-Feel Good Soup.mp3 - resampled - shape: (203676,), sr: 2048
ver2software-app-1  | Preprocessing, Feature Extraction for ./audio/오준성-09-Feel Good Soup.mp3 done with time: 3.1304426193237305s
ver2software-app-1  | Match process start for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-09-Feel Good Soup.mp3
ver2software-app-1  | Matching Algorithm video shape: (7068, 32), audio shape: (398, 32)
ver2software-app-1  | Preprocessing, Feature Extraction Start for ./audio/승희 (오마이걸)-01-You Are.mp3
ver2software-app-1  | ./audio/승희 (오마이걸)-01-You Are.mp3 - shape: (9855983,), sr: 44100
ver2software-app-1  | ./audio/승희 (오마이걸)-01-You Are.mp3 - resampled - shape: (457688,), sr: 2048
ver2software-app-1  | Preprocessing, Feature Extraction for ./audio/승희 (오마이걸)-01-You Are.mp3 done with time: 5.270148277282715s
ver2software-app-1  | Match process start for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/승희 (오마이걸)-01-You Are.mp3
ver2software-app-1  | Matching Algorithm video shape: (7068, 32), audio shape: (894, 32)
ver2software-app-1  | Preprocessing, Feature Extraction Start for ./audio/오준성-18-The Man In A Suit.mp3
ver2software-app-1  | ./audio/오준성-18-The Man In A Suit.mp3 - shape: (5841263,), sr: 44100
ver2software-app-1  | ./audio/오준성-18-The Man In A Suit.mp3 - resampled - shape: (271251,), sr: 2048
ver2software-app-1  | Preprocessing, Feature Extraction for ./audio/오준성-18-The Man In A Suit.mp3 done with time: 3.96024227142334s
ver2software-app-1  | Match process start for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-18-The Man In A Suit.mp3
ver2software-app-1  | Matching Algorithm video shape: (7068, 32), audio shape: (530, 32)
ver2software-app-1  | Preprocessing, Feature Extraction Start for ./audio/오준성-31-Nothing In My World.mp3
ver2software-app-1  | ./audio/오준성-31-Nothing In My World.mp3 - shape: (5444975,), sr: 44100
ver2software-app-1  | ./audio/오준성-31-Nothing In My World.mp3 - resampled - shape: (252848,), sr: 2048
ver2software-app-1  | Preprocessing, Feature Extraction for ./audio/오준성-31-Nothing In My World.mp3 done with time: 3.4876418113708496s
ver2software-app-1  | Match process start for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-31-Nothing In My World.mp3
ver2software-app-1  | Matching Algorithm video shape: (7068, 32), audio shape: (494, 32)
ver2software-app-1  | Preprocessing, Feature Extraction Start for ./audio/오준성-14-Singing Bird.mp3
ver2software-app-1  | ./audio/오준성-14-Singing Bird.mp3 - shape: (5955311,), sr: 44100
ver2software-app-1  | ./audio/오준성-14-Singing Bird.mp3 - resampled - shape: (276554,), sr: 2048
ver2software-app-1  | Preprocessing, Feature Extraction for ./audio/오준성-14-Singing Bird.mp3 done with time: 3.848504066467285s
ver2software-app-1  | Match process start for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-14-Singing Bird.mp3
ver2software-app-1  | Matching Algorithm video shape: (7068, 32), audio shape: (541, 32)
ver2software-app-1  | Match process done for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-04-Brand New-Day.mp3 with time: 196.89557147026062s
ver2software-app-1  | Match process done for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-09-Feel Good Soup.mp3 with time: 198.63251209259033s
ver2software-app-1  | Match process done for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-31-Nothing In My World.mp3 with time: 194.90334367752075s
ver2software-app-1  | Match process done for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/승희 (오마이걸)-01-You Are.mp3 with time: 204.21112966537476s
ver2software-app-1  | Match process done for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-18-The Man In A Suit.mp3 with time: 200.58395624160767s
ver2software-app-1  | Match process done for ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3 -- ./audio/오준성-14-Singing Bird.mp3 with time: 195.65312838554382s
ver2software-app-1  | Results:
ver2software-app-1  | Video: ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3, Audio: ./audio/오준성-04-Brand New-Day.mp3, Matched segments: [('0:0', '2:47'), ('4:21', '13:8'), ('13:54', '14:22'), ('15:21', '20:25'), ('21:36', '22:28'), ('23:6', '27:33'), ('28:15', '29:27')]
ver2software-app-1  | Video: ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3, Audio: ./audio/오준성-09-Feel Good Soup.mp3, Matched segments: [('0:23', '1:11'), ('10:18', '10:24'), ('12:8', '12:27'), ('17:7', '17:13'), ('17:14', '17:20'), ('19:23', '19:49')]
ver2software-app-1  | Video: ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3, Audio: ./audio/승희 (오마이걸)-01-You Are.mp3, Matched segments: [('0:22', '0:29'), ('19:11', '19:49'), ('29:21', '29:27')]    
ver2software-app-1  | Video: ./converted_video/사랑의 온도.E01.170918.720p-NEXT.mp3, Audio: ./audio/오준성-18-The Man In A Suit.mp3, Matched segments: [('0:26', '1:1'), ('9:58', '10:38'), ('17:13', '18:25')]     
ver2software-app-1 exited with code 0
```

The Result file

사랑의 온도.E01.170918.720p-NEXT_report.txt
```
Audio: 오준성-04-Brand New-Day
Matched segments: [('0:0', '2:47'), ('4:21', '13:8'), ('13:54', '14:22'), ('15:21', '20:25'), ('21:36', '22:28'), ('23:6', '27:33'), ('28:15', '29:27')]

Audio: 오준성-09-Feel Good Soup
Matched segments: [('0:23', '1:11'), ('10:18', '10:24'), ('12:8', '12:27'), ('17:7', '17:13'), ('17:14', '17:20'), ('19:23', '19:49')]

Audio: 승희 (오마이걸)-01-You Are
Matched segments: [('0:22', '0:29'), ('19:11', '19:49'), ('29:21', '29:27')]

Audio: 오준성-18-The Man In A Suit
Matched segments: [('0:26', '1:1'), ('9:58', '10:38'), ('17:13', '18:25')]
```
좀 난잡하다 싶으면 threshold를 낮추고, 너무 오래 걸린다 싶으면 sr을 낮추셈.

시간 계산은, 위에서 대충 한쌍 비교에 200초 걸렸으니 `영상 개수` x `음악 개수` x `200초` / `0.8코어개수` 정도 걸린다 보면 될듯.

예를들어 영상 100개, 음악 100개, 본인코어 16이면 100 * 100 * 200 / 12 = 46시간...ㅋㅋ
