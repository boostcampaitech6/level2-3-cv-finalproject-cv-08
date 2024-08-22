<script>
  import ButtonStyleFilled from "../join/ButtonStyleFilled.svelte";
  import RequestFilled from "../../components/button/request_filled.svelte";
  import PlaceholderImage from "./PlaceholderImage.svelte";
  import Header from "../../components/header/header_login.svelte";
  import StarRating from "../../components/rating/StarRating.svelte";
  import SaveImage from "../../components/button/result_save.svelte";
  import Survey from "../../components/survey/survey.svelte";
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let gt_stretch_path_m = "https://storage.makezenerator.com:9000/voice2face-public/site/result/tae_24fps_square.mp4"; 
  let gt_stretch_path_w = "https://storage.makezenerator.com:9000/voice2face-public/site/result/hj_24fps_square.mp4"; 
  let fail_path = "https://storage.makezenerator.com:9000/voice2face-public/site/result/sad.png"; 
  let results = [];
  let id;
  let latest_id;
  let gender;
  let token = null;
  
  onMount(async () => {
      token = sessionStorage.getItem('auth_token'); 
      if (!token) {
      alert(`세션이 만료되었습니다.\n다시 로그인 해주세요.`);
      goto('/');
      return
    }
      gender =sessionStorage.getItem('gender');
      id = sessionStorage.getItem('id');
      latest_id = sessionStorage.getItem('latest_id');

    
    const response = await fetch(`https://api.makezenerator.com/api/v1/mz-request/${id}/mz-result/${latest_id}`, {
      method: 'GET',
      headers: {
                'Token': token,
      },
      
    });

    if (response.ok) {
      const data = await response.json();
      results = data.mz_result; 
    } else if(response.status === 400) {
      alert("데이터베이스 에러");
    }
      else {
      console.error('데이터를 가져오는 데 실패했습니다.');
      alert("요청 중 에러가 발생했습니다.")
    }
  });

  


</script>
<div
style="
  background: var(--neutral-0, #ffffff);
  padding: 0px 0px 120px 0px;
  display: flex;
  flex-direction: column;
  gap: 30px;
  align-items: center; 
  justify-content: flex-start; 
  width: 100%; 
  height: auto;
  position: relative;
"
>
  <Header/>
  <img
    class="image-22"
    style="
      flex-shrink: 0;
      width: 196px;
      position: relative;
      object-fit: cover;
    "
    src="/logo/logo1.png"
    alt="logo"
  />
  <div
    style="
      display: flex;
      flex-direction: column;
      gap: 159px;
      align-items: center;
      justify-content: flex-start;
      flex-shrink: 0;
      position: relative;
    "
  >
    <div
      style="
        display: flex;
        flex-direction: row;
        gap: 211px;
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
          gap: 13px;
          align-items: center;
          justify-content: flex-start;
          flex-shrink: 0;
          position: relative;
        "
      >
        <div
          style="
            display: flex;
            flex-direction: column;
            gap: 15px;
            align-items: center;
            justify-content: flex-start;
            flex-shrink: 0;
            position: relative;
          "
        >
          <div
            style="
              display: flex;
              flex-direction: column;
              gap: 18px;
              align-items: flex-start;
              justify-content: flex-start;
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
                width: 294px;
                height: 40px;
              "
            >
              Voice
            </div>
            <div
              style="
                color: #8c8686;
                text-align: center;
                font-family: var(
                  --body-large-font-family,
                  'DmSans-Regular',
                  sans-serif
                );
                font-size: var(--body-large-font-size, 20px);
                line-height: var(--body-large-line-height, 32px);
                font-weight: var(--body-large-font-weight, 400);
                position: relative;
                width: 294px;
              "
            >
              목소리에 어울리는 얼굴
            </div>
          </div>
          <PlaceholderImage
            style="flex-shrink: 0; width: 390px; height: 390px"
            targetPath={results.voice_image_url}
          ></PlaceholderImage>
        </div>
        <div
          style="
            display: flex;
            flex-direction: row;
            gap: 70px;
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
              align-items: center;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
          <div
            style="
              display: flex;
              flex-direction: row;
              gap: 20px;
              align-items: flex-end;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
          <StarRating ABtype='voice' result_id={id} latest_id={latest_id} />
          <SaveImage targetImage= {results.voice_image_url} fileName="voice"/>
            
          </div>
            
          </div>
          
        </div>
      </div>
      <div
        style="
          display: flex;
          flex-direction: column;
          gap: 13px;
          align-items: center;
          justify-content: flex-start;
          flex-shrink: 0;
          position: relative;
        "
      >
        <div
          style="
            display: flex;
            flex-direction: column;
            gap: 15px;
            align-items: center;
            justify-content: flex-start;
            flex-shrink: 0;
            position: relative;
          "
        >
          <div
            style="
              display: flex;
              flex-direction: column;
              gap: 18px;
              align-items: flex-start;
              justify-content: flex-start;
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
                width: 294px;
                height: 40px;
              "
            >
              Condition
            </div>
            <div
              style="
                color: #8c8686;
                text-align: center;
                font-family: var(
                  --body-large-font-family,
                  'DmSans-Regular',
                  sans-serif
                );
                font-size: var(--body-large-font-size, 20px);
                line-height: var(--body-large-line-height, 32px);
                font-weight: var(--body-large-font-weight, 400);
                position: relative;
                width: 294px;
              "
            >
              성별, 나이만으로 만들어진 얼굴
            </div>
          </div>
          <PlaceholderImage
            style="flex-shrink: 0; width: 390px; height: 390px"
            targetPath={results.condition_image_url}
          ></PlaceholderImage>
        </div>
        <div
          style="
            display: flex;
            flex-direction: row;
            gap: 70px;
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
              align-items: center;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
          <div
            style="
              display: flex;
              flex-direction: row;
              gap: 20px;
              align-items: flex-end;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
          <StarRating ABtype= 'condition' result_id={id} latest_id={latest_id}/>
          <SaveImage targetImage={results.condition_image_url} fileName="condition"/>
            
          </div>
            
          </div>
          
        </div>
      </div>
    </div>
    <div
      style="
        display: flex;
        flex-direction: column;
        gap: 119px;
        align-items: center;
        justify-content: flex-start;
        flex-shrink: 0;
        position: relative;
      "
    >
      <div
        style="
          display: flex;
          flex-direction: column;
          gap: 10px;
          align-items: center;
          justify-content: flex-start;
          flex-shrink: 0;
          position: relative;
        "
      >
        <div
          style="
            color: #000000;
            text-align: center;
            font-family: 'DmSans-Bold', sans-serif;
            font-size: 52px;
            line-height: 76px;
            font-weight: 700;
            position: relative;
            width: 742px;
            height: 65px;
          "
        >
          Service Coming soon
        </div>
        <div
          style="
            color: #8c8686;
            text-align: center;
            font-family: var(
              --body-large-font-family,
              'DmSans-Regular',
              sans-serif
            );
            font-size: var(--body-large-font-size, 20px);
            line-height: var(--body-large-line-height, 32px);
            font-weight: var(--body-large-font-weight, 400);
            position: relative;
            width: 615px;
            height: 150px;
          "
        >
          생성된 이미지를 영상에 입힐 수 있습니다
          
        </div>
        <div
          style="
            display: flex;
            flex-direction: row;
            gap: 77px;
            align-items: flex-end;
            justify-content: flex-start;
            flex-shrink: 0;
            position: relative;
          "
        >
          <div
            style="
              flex-shrink: 0;
              width: 393px;
              height: 498px;
              position: relative;
            "
          >
            <div
              style="
                display: flex;
                flex-direction: column;
                gap: 18px;
                align-items: flex-start;
                justify-content: flex-start;
                position: absolute;
                left: 49.5px;
                top: 0px;
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
                  width: 294px;
                  height: 40px;
                "
              >
                Original
              </div>
              <div
                style="
                  color: #8c8686;
                  text-align: center;
                  font-family: var(
                    --body-large-font-family,
                    'DmSans-Regular',
                    sans-serif
                  );
                  font-size: var(--body-large-font-size, 20px);
                  line-height: var(--body-large-line-height, 32px);
                  font-weight: var(--body-large-font-weight, 400);
                  position: relative;
                  width: 294px;
                "
              >
                스트레칭 동영상
              </div>
            </div>
            {#if gender == "man"} <video 
            style="
            width: 393px;
            height: 393px;
            position: absolute;
            left: 0px;
            top: 105px;
          "
       src= {gt_stretch_path_m} type="video/mp4" autoplay loop muted />
       {:else}
       <video 
                style="
                width: 393px;
                height: 393px;
                position: absolute;
                left: 0px;
                top: 105px;
              "
           src= {gt_stretch_path_w} type="video/mp4" autoplay loop muted />
       
       {/if}
            
          </div>
          <div
            style="
              flex-shrink: 0;
              width: 393px;
              height: 498px;
              position: relative;
            "
          >
            <div
              style="
                display: flex;
                flex-direction: column;
                gap: 18px;
                align-items: flex-start;
                justify-content: flex-start;
                position: absolute;
                left: 49.5px;
                top: 0px;
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
                  width: 294px;
                  height: 40px;
                "
              >
                Voice
              </div>
              <div
                style="
                  color: #8c8686;
                  text-align: center;
                  font-family: var(
                    --body-large-font-family,
                    'DmSans-Regular',
                    sans-serif
                  );
                  font-size: var(--body-large-font-size, 20px);
                  line-height: var(--body-large-line-height, 32px);
                  font-weight: var(--body-large-font-weight, 400);
                  position: relative;
                  width: 294px;
                "
              >
                목소리에 어울리는 얼굴
              </div>
            </div>
            {#if results.voice_gif_url == null}
            <PlaceholderImage
            style="
            flex-shrink: 0; 
            width: 393px;
            height: 393px;
            <!-- position: absolute;
            left: 0px;
            top: 105px; -->
                "
            targetPath={fail_path}
          ></PlaceholderImage>
            {:else}

            <video 
                style="
                width: 393px;
                height: 393px;
                position: absolute;
                left: 0px;
                top: 105px;
              "
            src= {results.voice_gif_url} type="video/mp4" autoplay loop muted />

            {/if}
            
            
          </div>
          <div
            style="
              flex-shrink: 0;
              width: 393px;
              height: 498px;
              position: relative;
            "
          >
            <div
              style="
                display: flex;
                flex-direction: column;
                gap: 18px;
                align-items: flex-start;
                justify-content: flex-start;
                position: absolute;
                left: 49.5px;
                top: 0px;
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
                  width: 294px;
                  height: 40px;
                "
              >
                Condition
              </div>
              <div
                style="
                  color: #8c8686;
                  text-align: center;
                  font-family: var(
                    --body-large-font-family,
                    'DmSans-Regular',
                    sans-serif
                  );
                  font-size: var(--body-large-font-size, 20px);
                  line-height: var(--body-large-line-height, 32px);
                  font-weight: var(--body-large-font-weight, 400);
                  position: relative;
                  width: 294px;
                "
              >
              성별, 나이만으로 만들어진 얼굴
              </div>
            </div>

            <video 
                style="
                width: 393px;
                height: 393px;
                position: absolute;
                left: 0px;
                top: 105px;
              "
           src= {results.condition_gif_url} type="video/mp4" autoplay loop muted />

          </div>
        </div>
      </div>
      <div
        style="display: flex; items-align: center; justify-contents: center ; gap: 50px;  position: static"
      >
      
      {#if results.updated_at == null}
        <RequestFilled
          styleVariant="filled"
          style="
            background: var(--7b95b7, #6b6b6b);
            width: 190px;
          "
          name="다시 생성하기"
        ></RequestFilled>
      {/if}
        <ButtonStyleFilled
          styleVariant="filled"
          style="
            background: var(--7b95b7, #6b6b6b);
            width: 190px;

          "
          targetPath="/resultlist"
          name="결과 목록 보기"
        ></ButtonStyleFilled>
      </div>
    </div>
  </div>
  {#if results.survey == 0}
  <div><br><br></div>
  <div
          style="
            color: #000000;
            text-align: center;
            font-family: 'DmSans-Bold', sans-serif;
            font-size: 52px;
            line-height: 76px;
            font-weight: 700;
            position: relative;
            width: 742px;
            height: 65px;
          "
        >
          설문조사
        </div>

  <div style="text-align:center; font-size: 18pt; "> 
    안녕하세요! 사용자의 목소리를 기반으로 가상의 얼굴을 생성하는 서비스, <br >
    <span><strong>Voice2Face</strong></span>를 개발 중인 <span><strong>Make Zenerator</strong></span>팀입니다.
    <br><br>
    저희는 온라인 상에서 얼굴을 드러내고 싶지 않은 사람들에게 목소리를 기반으로 생성한 얼굴을 제공하여, 
    <br />
    목소리와 이미지 간의 이질감을 없애고 사생활을 보장받으며 온라인 상에서 활동할 수 있도록 하는 서비스를 제공하고자 합니다.
    <br>
    <br />
    서비스 품질 향상을 위해 지금까지의 서비스 이용 경험을 바탕으로 아래의 설문 조사에 참여해주시면 감사드리겠습니다.
    <br />
    설문 예상 소요 시간은 <span><strong>약 5분 내외</strong></span>이며  
    <br /> 
    참여하신 분들 중 추첨을 통해 5분께 <span><strong>스타벅스 카페 아메리카노</strong></span> 기프티콘을 드릴 예정입니다.
    <br />
    (설문은 생성된 이미지 결과별로 제출할 수 있습니다.)
    </div>

    <div 
      style="
      display: flex; 
      flex-direction: column; 
      align-items: center; 
      justify-content: center; 
      text-align: center; 
      width: 100%; 
    ">
    <div style="items-align:center; ">
      
      <Survey survey_id={id} survey_latest_id={latest_id} />
    </div>

    
</div>
{/if}
</div>




