<script>
    import ButtonStyleFilled from "./join/ButtonStyleFilled.svelte";
    import ButtonStyleOutlined from "./join/ButtonStyleOutlined.svelte";
    import Header from "../components/header/header_non.svelte";

  </script>
  <div
  style="{'background: var(--neutral-0, #ffffff);padding: 0px 0px 120px 0px; display: flex; flex-direction: column; gap: 100px; align-items: center; justify-content: flex-start;  position: relative; ' }"
  >
  <Header/>
 <div>
    <div
      style="
        display: flex;
        flex-direction: column;
        gap: 120px;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        position: relative;
      "
      name="생성하기"
    >
      <div
        style="
          display: flex;
          flex-direction: row;
          gap: 110px;
          align-items: center;
          justify-content: flex-end;
          flex-shrink: 0;
          width: 1200px;
          position: relative;
        "
      >
        <div
          style="
            display: flex;
            flex-direction: column;
            gap: 24px;
            align-items: flex-start;
            justify-content: flex-start;
            flex-shrink: 0;
            width: 612px;
            position: relative;
          "
        >
          <div
            style="
              display: flex;
              flex-direction: column;
              gap: 16px;
              align-items: flex-start;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
            <div
              style="
                display: flex;
                flex-direction: column;
                gap: 8px;
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
                  font-family: var(
                    --title-small-font-family,
                    'DmSans-Bold',
                    sans-serif
                  );
                  font-size: var(--title-small-font-size, 32px);
                  line-height: var(--title-small-line-height, 40px);
                  font-weight: var(--title-small-font-weight, 700);
                  position: relative;
                  width: 612px;
                "
              >
                10초의 새로운 경험
              </div>
              <div
                style="
                  color: #000000;
                  text-align: left;
                  font-family: var(
                    --title-large-font-family,
                    'DmSans-Bold',
                    sans-serif
                  );
                  font-size: var(--title-large-font-size, 60px);
                  line-height: var(--title-large-line-height, 76px);
                  font-weight: var(--title-large-font-weight, 700);
                  position: relative;
                  width: 612px;
                "
              >
                내 목소리 다른 얼굴
              </div>
            </div>
            <div
              style="
                color: #8c8686;
                text-align: left;
                font-family: var(
                  --body-large-font-family,
                  'DmSans-Regular',
                  sans-serif
                );
                font-size: var(--body-large-font-size, 20px);
                line-height: var(--body-large-line-height, 32px);
                font-weight: var(--body-large-font-weight, 400);
                position: relative;
                width: 612px;
              "
            >
              Introducing MZ team&#039;s new voice to face technology
              <br />
              where you can experience your own impressions and characters with
              your voice.
            </div>
          </div>
          <div
            style="
              display: flex;
              flex-direction: row;
              gap: 24px;
              align-items: flex-start;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
            <ButtonStyleFilled
              styleVariant="filled"
              style="background: #000000; border-color: #000000; flex-shrink: 0"
              name="나의 다른 모습 체험하기"
              targetPath="/login"
            ></ButtonStyleFilled>
            <ButtonStyleOutlined
              style="border-color: #000000; flex-shrink: 0"
              name="회원가입"
              targetPath="/join"
            ></ButtonStyleOutlined>


          </div>
        </div>
        <video autoplay loop muted style="width:40% ">
          <source src="https://storage.makezenerator.com:9000/voice2face-public/site/main/main_sample.mp4" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      </div>
      <div
        style="
          display: flex;
          flex-direction: column;
          gap: 20px;
          align-items: flex-end;
          justify-content: center;
          flex-shrink: 0;
          position: relative;
        "
      >
        

          <img
            class="group3"
            style="
              flex-shrink: 0;
              width: 300px;
              height: 100%;
              position: relative;
              overflow: visible;
              top: -18px;
            "
            src="/logo/boostcampLogo.jpg"
            alt="boostcamp"
          />

      </div>
    </div>
  </div>
  </div>