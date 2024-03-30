# 🔊목소리로 가상 얼굴 생성 서비스 [너의 목소리가 보여]

  <img  src="https://img.shields.io/badge/figma-_F24E1E?style=for-the-badge&logo=figma&logoColor=white">
  <img src="https://img.shields.io/badge/svelte-FF3E00?style=for-the-badge&logo=svelte&logoColor=white">


## Project Structure

```
frontend
┣ src
┃ ┣ components
┃ ┃ ┣ button
┃ ┃ ┃ ┣ basic_filled.svelte
┃ ┃ ┃ ┣ moving_filled.svelte
┃ ┃ ┃ ┣ request_filled.svelte
┃ ┃ ┃ ┗ result_save.svelte
┃ ┃ ┣ header
┃ ┃ ┃ ┣ header_login.svelte
┃ ┃ ┃ ┗ header_non.svelte
┃ ┃ ┣ image
┃ ┃ ┃ ┣ PlaceholderImage.svelte
┃ ┃ ┃ ┗ SocialProperty1Github.svelte
┃ ┃ ┣ modal
┃ ┃ ┃ ┗ basic_modal.svelte
┃ ┃ ┣ rating
┃ ┃ ┃ ┣ Star.svelte
┃ ┃ ┃ ┗ StarRating.svelte
┃ ┃ ┗ survey
┃ ┃   ┣ input_area.svelte
┃ ┃   ┗ survey.svelte
┃ ┣ routes
┃ ┃ ┣ aboutus
┃ ┃ ┃ ┗ +page.svelte
┃ ┃ ┣ home
┃ ┃ ┃ ┗ +page.svelte
┃ ┃ ┣ infogather
┃ ┃ ┃ ┣ +page.svelte
┃ ┃ ┃ ┗ VoiceButtonDefaultVariant3.svelte
┃ ┃ ┣ join
┃ ┃ ┃ ┣ +page.svelte
┃ ┃ ┃ ┣ ButtonStyleFilled.svelte
┃ ┃ ┃ ┣ ButtonStyleOutlined.svelte
┃ ┃ ┃ ┣ PlaceholderImage.svelte
┃ ┃ ┃ ┣ radio.svelte
┃ ┃ ┃ ┣ RadioBigDefault.svelte
┃ ┃ ┃ ┗ RadioSmallS.svelte
┃ ┃ ┣ loading
┃ ┃ ┃ ┗ +page.svelte
┃ ┃ ┣ login
┃ ┃ ┃ ┣ +page.svelte
┃ ┃ ┃ ┗ PlaceholderImage.svelte
┃ ┃ ┣ maintenance
┃ ┃ ┃ ┗ +page.svelte
┃ ┃ ┣ result
┃ ┃ ┃ ┣ +page.svelte
┃ ┃ ┃ ┗ PlaceholderImage.svelte
┃ ┃ ┗ resultlist
┃ ┃ ┃ ┣ +page.svelte
┃ ┃ ┃ ┗ ButtonStyleFilled.svelte
┃ ┃ ┣ +layout.svelte
┃ ┃ ┣ +page.js
┃ ┃ ┣ +page.svelte
┃ ┃ ┣ styles.css
┃ ┣ app.html
┃ ┣ app.pcss
┃ ┗ hooks.js
┣ static
┣ .gitignore
┣ .npmrc
┣ Dockerfile
┣ package.json
┣ package-lock.json
┣ postcss.config.cjs
┣ README.md
┣ svelte.config.js
┣ tailwind.config.cjs
┗ vite.config.js
```
## Usage

  
### `src` 
#### `components`
: 페이지 내부에 포함할 컴포넌트를 모듈화 하기 위해 보관해둔 폴더
 - `button`: 화면 변경이나,  input event 등의 trigger로 사용하기 위한 버튼을 보관한 폴더
 - `header`: 웹사이트 header 보관 폴더
 - `image`: 웹에 사용되는 이미지 style을 지정할 폴더
 - `modal`: 주의사항을 표시할 modal을 보관한 폴더
 - `rating`: 별점 표시, 전송을 위한 컴포넌트를 보관한 폴더
 - `survey`: 설문조사 항목에 대한 컴포넌트를 보관한 폴더

#### `routes` 
: 서비스에 사용된 페이지를 담아둔 폴더

 - `aboutus`: 팀, 팀원 소개를 위한 페이지
 - `home`: 로그인 후 생성요청이나, 결과 확인으로 이동할 수 있는 화면
 - `infogather`: 사용자가 생성요청을 보낼 수 있는 페이지
   - `VoiceButtonDefaultVariant3.svelte`: 음성 녹음 및 Blob을 생성하기 위한 모듈
 - `join`: 회원가입을 위한 페이지
 - `loading`: 사용자가 이미지 생성 요청 후 넘어갈 수 있는 페이지로 결과나 `home`화면으로 이동할 수 있다.
 - `login`: 로그인 페이지
 - `maintenance`: 서비스 점검 시 사용될 페이지
 - `result`: 결과를 확인할 수 있는 페이지
 - `resultlist`: 결과 목록 페이지
 
#### `hooks.js`
: 서비스 점검 시 모든 화면을 maintenance 화면으로 이동하는 event 를 발생시킬 훅을 추가하는 파일
### `static`
: 서비스에 사용된 이미지를 보관해둔 폴더


## Getting Started
This project was developed and tested on the following operating systems:
- **Linux**: Ubuntu 20.04 LTS
- **Windows**: Windows 11 Home

### 1. Install Requirements

To run this project, you'll need Node.js installed on your system. We recommend using NVM (Node Version Manager) to manage your Node.js versions.
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
source ~/.bashrc
nvm install 20.11.1
```

This project uses Tailwind CSS, Flowbite, and Svelte routing for UI and navigation.
```
# basic package
npm install
npx svelte-add@latest tailwindcss
npm install -D tailwindcss svelte-routing flowbite-svelte flowbite
```
### 2. Developing

To start the development server, run:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

### 3. Building

To create a production build, use:

```
npm run build
```
  
## Links
- [Wireframe](https://www.figma.com/file/MBWE1CthewJVCl0KH8xEcM/%5BV1%5D-%ED%99%94%EB%A9%B4-%EA%B5%AC%EC%84%B1?type=whiteboard&node-id=0:1&t=jPWmEIfP3RobQG6G-1)
- [Prototyping](https://www.figma.com/file/fN6DWRmoszsytULLaZ4cni/Voice2Face-V1?type=design&node-id=1603:2&mode=design&t=jPWmEIfP3RobQG6G-1)
- [Origin github](https://github.com/Make-Zenerator/voice2face-frontend.git)