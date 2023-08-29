<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->
<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">Understanding Short-Videos Using GPT</h3>

  <p align="center">
    project_description
    <br />

    
  </p>
</div>


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

Install ffmpeg 
* for mac
  ```sh
  brew install ffmpeg
  ```
* for ubuntu
  ```sh
  sudo apt-get install ffmpeg
  ```
### Installation

1. Get a OpenAI ChatGPT API Key at [https://chat.openai.com](https://chat.openai.com)
   and a Azure speech API key at [https://portal.azure.com](https://portal.azure.com)
2. Clone the repo
   ```sh
   git clone https://github.com/oaapao/GPT-based-Short-Video-Understanding.git
   ```
3. Install python packages
   ```sh
   conda create -n gpt python=3.11
   conda activate gpt
   pip install -r requirements.txt
   ```
4. Enter your API Key in `~/.bashrc` or `~/.zshrc`
   ```sh
   vi ~/.zshrc
   export CHATGPT_AK={your_sk}
   export AZURE_KEY={your_sk}
   ```



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.


1. Prepare your video data
2. Changing your prompt in `chat_with_function_call.py`
3. Run `chat_with_function_call.py`
```python
python chat_with_function_call.py
```
<!-- ROADMAP -->
## Roadmap
- [x] Convert video to speech 
- [x] Convert speech to text 
- [x] ChatGPT function call works
- [ ] Add `download_douyin` in `available_functions` and `functions`
- [ ] Automate search video by keyword in Douyin (web crawler related)
- [ ] Upgrade prompt

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


