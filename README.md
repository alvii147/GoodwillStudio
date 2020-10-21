[![Video_Thumbnail](http://i3.ytimg.com/vi/s4MnD7pdQyg/maxresdefault.jpg)](https://youtu.be/s4MnD7pdQyg)
# sunhacks 2020 (Best Use of Google Cloud - 2nd Place)
## Inspiration
**Tourette syndrome (TS)** is a neurological disorder characterized by repetitive, stereotyped, involuntary movements and vocalizations called tics. The disorder is named after Dr. Georges Gilles de la Tourette, the pioneering French neurologist who first described the condition in 1885. Studies show that around 1 out of every 162 children (0.6%) develop some form of TS, but only about 1 out of every 360 children (0.3%) between the ages of 6 and 17 are diagnosed in US, meaning about half the children in US are undiagnosed.

![Prevalence of Diagnosed Tourette Syndrome](https://www.cdc.gov/ncbddd/tourette/images/tourette-map-prevalence600px.jpg)

Most tics may be categorized as either motor tics - involuntary movements caused by spasm-like contractions of muscles, most commonly involving the face, mouth, eyes, head, neck or shoulders - or vocal tics - words and sounds uttered unintentionally. A typical symptom of vocal TS is **Coprolalia**. Coprolalia, the involuntary and uncontrollable use of foul or obscene language, is reported to occur in as much as 60% of people diagnosed with TS. Unfortunately, undiagnosed victims of TS with symptoms of Coprolalia are often subject to public ridicule due to their excessive use of foul language.

That's exactly where ***Goodwill Studio*** looks to make a difference!

## What it does
***Goodwill Studio*** is a desktop tool intended to allow users to **detect and censor profane language from voice recordings or microphones**. Using machine learning to extract text from speech and natural language processing to detect profane language, ***Goodwill Studio*** efficiently detects slangs and censors offensive words from speech recordings, in hopes of providing a clean method of communication for people affected by TS and Coprolalia. With audio waveform support and accurate audio transcription, ***Goodwill Studio*** allows users to record audio, export censored clips and provides censored transcription.

## How I built it
***Goodwill Studio*** is a desktop application written by integrating advance styling features with the **PyQt5** library. Using **SciPy** and **PyAudio** libraries to decode and record audio files, I had to incorporate a threaded application to allow smooth transition between the GUI and the internal processes. In order to detect offensive language in speech, I utilized the **Google Cloud Speech Client Library** in **Python** to implement realistic speech to text conversion. I then made use of **better_profanity**, a Python library that uses natural language processing to recognize profanity, to detect and filter out offensive words.

## Challenges I ran into
In terms of the building process, the most challenging aspect of this project has been the implementation of multi-threaded processes. When it comes to GUI development, it is crucial to develop threading in order to avoid unresponsive user interface components. Additionally, deciding the most efficient way of implementing the machine learning aspect of this application was equally challenging. Most problems have multiple solutions using multiple methods, but only one out of them is worth the most in effectiveness.

## Accomplishments that I'm proud of and what I learned
This was my first desktop application at a hackathon and I worked on the entire project by myself. I am extremely proud to have developed a professional-looking application, and excited to imagine the people this project could potentially help!

## What's next for ***Goodwill Studio***
***Goodwill Studio*** was a lot of fun to work on. Having said that, there are a lot of aspects of this application that I would like to improve and countless features that I plan on adding. These include but are not limited to:
* Real-time recording and streaming services
* Support for censoring non-speech sounds for TS patients
* Cross-platform integration