<script>
  import BasicFilled from "../../components/button/basic_filled.svelte";
  import PlaceholderImage from "./PlaceholderImage.svelte";
  import Header from "../../components/header/header_non.svelte";
  import { goto } from '$app/navigation';

  let login_email;
  let login_pswd;
  let targetPath = "/home";

  async function login() {
    const formData = new FormData();
    formData.append('email', login_email);
    formData.append('password', login_pswd);

    try{
        const response = await fetch('https://api.makezenerator.com/api/v1/auth', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json(); // 백엔드로부터 받은 데이터를 JSON으로 파싱
            const { token, email } = data; // 파싱된 JSON 객체에서 token과 email을 추출

            // 토큰과 이메일을 로컬 스토리지에 저장
            sessionStorage.setItem('auth_token', token);

            alert(`로그인 성공!`);


            goto(targetPath); // 사용자를 홈 페이지로 리다이렉트
        } else {
            alert('로그인 실패 \n 이메일과 비밀번호를 확인해주세요');
        }
    } catch (error) {
      console.error('로그인 중 에러 발생:', error);
      alert('로그인 중 에러가 발생했습니다.');
    }
  }


</script>
<form on:submit|preventDefault={login} style="{'background: var(--neutral-0, #ffffff);padding: 0px 0px 120px 0px; display: flex; flex-direction: column; gap: 120px; align-items: center; justify-content: flex-start; height: 845px; position: relative; '}">
<div
  style="{'background: var(--neutral-0, #ffffff); display: flex; flex-direction: column; gap: 160px; align-items: center; justify-content: flex-start; height: 845px; position: relative; ' }"
>
  <Header/>
  <div
    style="
      display: flex;
      flex-direction: row;
      gap: 82px;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      width: 1103px;
      height: 429px;
      position: relative;
    "
  >
    <div
      style="
        display: flex;
        flex-direction: row;
        gap: 82px;
        align-items: center;
        justify-content: flex-start;
        flex-shrink: 0;
        height: 423px;
        position: relative;
      "
    >
      <div
        style="
          display: flex;
          flex-direction: row;
          gap: 82px;
          align-items: center;
          justify-content: flex-start;
          flex-shrink: 0;
          height: 401px;
          position: relative;
        "
      >
        <div
          style="
            background: #ffffff;
            border-radius: 10px;
            border-style: solid;
            border-color: #878787;
            border-width: 0.5px;
            padding: 47px 0px 47px 0px;
            display: flex;
            flex-direction: row;
            gap: 10px;
            align-items: flex-start;
            justify-content: flex-start;
            flex-shrink: 0;
            width: 451px;
            height: 395px;
            position: relative;
            box-shadow: 0px 4px 64px 0px rgba(0, 0, 0, 0.05);
            overflow: hidden;
          "
        >
          <div
            style="
              display: flex;
              flex-direction: column;
              gap: 20px;
              align-items: center;
              justify-content: center;
              flex-shrink: 0;
              position: relative;
            "
          >
            <div
              style="
                display: flex;
                flex-direction: column;
                gap: 20px;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                position: relative;
              "
            >
              <div
                style="
                  color: #000000;
                  text-align: center;
                  font-family: 'DmSans-Bold', sans-serif;
                  font-size: 46px;
                  line-height: 40px;
                  font-weight: 700;
                  position: relative;
                  width: 451px;
                  height: 40px;
                "
              >
                로그인
              </div>
              <div
                style="
                  display: flex;
                  flex-direction: column;
                  gap: 10px;
                  align-items: flex-start;
                  justify-content: flex-start;
                  flex-shrink: 0;
                  position: relative;
                "
              >
                <div
                  style="
                    color: #000000;
                    text-align: left;
                    font-family: 'DmSans-Medium', sans-serif;
                    font-size: 19px;
                    line-height: 40px;
                    font-weight: 500;
                    position: relative;
                    width: 125px;
                    height: 23px;
                    display: flex;
                    align-items: center;
                    justify-content: flex-start;
                  "
                >
                  이메일 주소
                </div>
                <div
                  style="
                    background: #ffffff;
                    border-radius: 10px;
                    border-style: solid;
                    border-color: #000000;
                    border-width: 1px;
                    padding: 1px 43px 1px 43px;
                    display: flex;
                    flex-direction: row;
                    gap: 10px;
                    align-items: center;
                    justify-content: flex-start;
                    flex-shrink: 0;
                    width: 337px;
                    position: relative;
                    overflow: hidden;
                  "
                >
                <input type='email' bind:value={login_email} placeholder="이메일 입력"
                style="
                  color: rgba(0, 0, 0, 0.4);
                  text-align: center;
                  font-family: 'DmSans-Medium', sans-serif;
                  font-size: 18px;
                  line-height: 30px;
                  font-weight: 500;
                  position: relative;
                  width: 100%;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  border: none;
                "
              />
                </div>
                <div
                  style="
                    color: #000000;
                    text-align: left;
                    font-family: 'DmSans-Medium', sans-serif;
                    font-size: 19px;
                    line-height: 40px;
                    font-weight: 500;
                    position: relative;
                    width: 125px;
                    height: 23px;
                    display: flex;
                    align-items: center;
                    justify-content: flex-start;
                  "
                >
                  비밀번호
                </div>
                <div
                  style="
                    background: #ffffff;
                    border-radius: 10px;
                    border-style: solid;
                    border-color: #000000;
                    border-width: 1px;
                    padding: 1px 43px 1px 43px;
                    display: flex;
                    flex-direction: row;
                    gap: 10px;
                    align-items: center;
                    justify-content: flex-start;
                    flex-shrink: 0;
                    width: 337px;
                    position: relative;
                    overflow: hidden;
                  "
                >
                <input type='password' bind:value={login_pswd} placeholder="비밀번호 입력"
                style="
                  color: rgba(0, 0, 0, 0.4);
                  text-align: center;
                  font-family: 'DmSans-Medium', sans-serif;
                  font-size: 18px;
                  line-height: 30px;
                  font-weight: 500;
                  position: relative;
                  width: 100%;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  margin: 0;
                  background: transparent;
                  -webkit-appearance: none;
                  border: none;
                "
              />
                </div>
              </div>
            </div>
            <BasicFilled
              styleVariant="filled"
              style=
              "background: var(--7b95b7, #6b6b6b);
              flex-shrink: 0"
              name="로그인"
              type="submit"
            ></BasicFilled>
          </div>
          <div
            style="
              background: #d9d9d9;
              flex-shrink: 0;
              width: 100px;
              height: 100px;
              position: relative;
            "
          ></div>
        </div>
        <PlaceholderImage
          style="flex-shrink: 0; width: 405px; height: 405px" 
          src="logo/login_f.png"
        ></PlaceholderImage>
      </div>
    </div>
  </div>
</div>

</form>