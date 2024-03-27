<script>
    import Radio from "../../routes/join/radio.svelte";
    import TextArea from "./input_area.svelte";
    import {goto} from '$app/navigation';
    export let style;
  
    
    let token = null;


    token = sessionStorage.getItem('auth_token'); 



    const SNS_time =[
        {value: 0, label: '1시간 미만'},
        {value: 1, label:'1시간 ~ 3시간 미만'},
        {value: 2, label: '3시간 ~ 5시간 미만'},
        {value: 3, label: '5시간 이상'},
    ]
    let SNS = null;

    let reason_img_rate; 
    
    const well_serviced = [
        {value: 0, label: '매우 아니다'},
        {value: 1, label: '아니다'},
        {value: 2, label: '그렇다'},
        {value: 3, label: '매우 그렇다'},
        {value: 4, label: '모르겠다'},
    ]
    let v2f = null;

    const dissatisfied_generated_image = [
        {value: 0, label: '외국인이라 어색하다'},
        {value: 1, label: '생성된 이미지가 깨끗하지 않다'},
        {value: 2, label: '목소리가 잘 반영된 것인지 의문스럽다'},
        {value: 3, label: '성별이 바뀌어 생성된 것 같다'},
    ] //checkbox

    let image_add_function;

    const face_to_gif_well = [
        {value: 0, label: '매우 아니다'},
        {value: 1, label: '아니다'},
        {value: 2, label: '그렇다'},
        {value: 3, label: '매우 그렇다'},
        {value: 4, label: '모르겠다'},
    ]
    let f2g= null;

    const more_based_gif = [
        {value: 1, label: '예'},
        {value: 0, label: '아니요'},
    ] //bool
    let mbg = null;

    const gif_based_additional_function = [
        {value: 0, label: '드라마/영화 명장면'},
        {value: 1, label: '예능 움짤'},
        {value: 2, label: '뮤직비디오'},
        {value: 3, label: '뉴스'},
    ] // checkbox
    
    const waiting_or_not = [
        {value: 0, label: '이정도면 기다릴 수 있다'},
        {value: 1, label: '대기하지 않을 것 같다'},
    ] //bool
    let won = null;

    const waiting_about = [
        {value: 0, label: '1분 이내 생성 결과 확인하기'},
        {value: 1, label: '생성된 결과를 가입한 이메일로 전달받기'},
        {value: 2, label: '예시 영상 구경하기'},
        {value: 3, label: '생성완료되면 카톡으로 알림받기'}
    ]

    const dissatified_service = [
        {value: 1, label: '있다'},
        {value: 0, label: '없다'},
    ] //bool

    let service = null;

    const agree = [
        {value: 0, label: '동의 안함'},
        {value: 1, label:  '동의 함'},

    ]
    let agree2 = null;

    let service_comments;
    
    let email=null;
    export let survey_id ;
    export let survey_latest_id;
    
    // 생성 얼굴 만족도
    let selectedValues1 = [];
    $: sortedSelectedValues1 = [...selectedValues1].sort((a, b) => a - b);
    $: selectedString1 = sortedSelectedValues1.join(", ");

    // 짤 추천
    let selectedValues2 = [];
    $: sortedSelectedValues2 = [...selectedValues2].sort((a, b) => a - b);
    $: selectedString2 = sortedSelectedValues2.join(", ");

    let selectedValues3 = [];
    $: sortedSelectedValues3 = [...selectedValues3].sort((a, b) => a - b);
    $: selectedString3 = sortedSelectedValues3.join(", ");


    async function handleSubmit() {

        if (SNS == null) {
          alert("1번 문항에 답변이 작성되지 않았습니다.");
          return 
        }
        else if (reason_img_rate == null) {
          alert("2번 문항에 답변이 작성되지 않았습니다.");
          return
        }
        else if (v2f == null) {
          alert("3번 문항에 답변이 작성되지 않았습니다.");
          return
        }
        else if (f2g == null) {
          alert("5번 문항에 답변이 작성되지 않았습니다.");
          return
        }
        else if (mbg == null) {
          alert("6번 문항에 답변이 작성되지 않았습니다.");
          return
        }
        else if (won == null) {
          alert("7번 문항에 답변이 작성되지 않았습니다.");
          return
        }
        else if (service == null) {
          alert("8번 문항에 답변이 작성되지 않았습니다.");
          return
        }

        const formData = new FormData;
        formData.append('sns_time', SNS);
        formData.append('user_phone', email);
        formData.append('image_rating_reason', reason_img_rate); ///
        formData.append('voice_to_face_rating', v2f);
        formData.append('dissatisfy_reason', selectedString1);
        formData.append('additional_function', image_add_function);
        formData.append('face_to_gif_rating', f2g); 
        formData.append('more_gif', mbg);
        formData.append('more_gif_type', selectedString2); ///
        formData.append('waiting',won);
        formData.append('waiting_improvement', selectedString3);
        formData.append('recommend', service);
        formData.append('opinion', service_comments);


    try {
      const response = await fetch(`https://api.makezenerator.com/api/v1/mz-request/${survey_id}/mz-result/${survey_latest_id}`, {
        method: 'POST',
        headers: {
            'Token':token,
        },
        body: formData,
      });

      if (response.ok) {
        alert("설문에 응해주셔서 감사합니다! \n더 좋은 서비스 제공을 위해 노력하는 Make Zenerator 되겠습니다.");
        goto('/home');
      }
      else {
        alert('Error ');
      }
      
    } catch (error) {
      console.error('Failed to submit the form:', error);
    }
  }

</script>

<style>
    .question {
        font-size: 24px;
        font-weight: bold;
    }

    .t_box {
        width: 30%;
        height:40px;
    }


    .survey-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    border-radius: 10px;
    box-shadow: 0 4px 64px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(135, 135, 135, 1);
    background-color: #fff;
    margin-top: 56px;
    letter-spacing: 0.5px;
    padding: 44px 60px;
    gap: 20px;
  }
  .checkboxContainer {
    display: flex; 
    flex-wrap: wrap; 
    justify-content: space-between; 
    width: 100%;
  }

  .checkboxRow {
    display: flex; 
    flex-direction: row; 
    flex-basis: 100%; 
    justify-content: space-around;
  }

  .checkboxLabel {
    font-size: 15pt; 
    flex-basis: 45%; 
    display: flex; 
    align-items: center; 
  }
  </style>

    


<form on:submit|preventDefault={handleSubmit} style="{'background: var(--neutral-0, #ffffff);padding: 0px 0px 120px 0px; display: flex; flex-direction: column; gap: 120px; align-items: center; justify-content: flex-start; position: relative; width: 1200px;'+ style}">

<div style="'font-size: 20pt">
    <div class= survey-container >
        <p class="question">1. SNS나 인터넷, 유튜브를 하루 평균 몇 시간 사용하시나요?</p>
        <Radio options={SNS_time} fontSize={20} legend=''  bind:userSelected={SNS}/>
    </div>
    <div class= survey-container>
        
        <p class="question">2. 생성된 이미지들에 대해 해당 별점을 주신 이유가 무엇인가요? </p>
        <TextArea bind:value={reason_img_rate} />
        <br>
        <p class="question"> 3. 목소리를 기반으로 생성된 얼굴이 본인의 목소리를 잘 반영한 것 같다 생각하시나요?</p>
        <Radio options={well_serviced} fontSize={20} legend=''  bind:userSelected={v2f} />
        <br>
        {#if v2f in [0, 1]}
        <p class="question">3+. 생성된 얼굴이 만족스럽지 않다면, 어떤 점이 불만족스러우신가요? (복수선택 가능)</p>
        <div class="checkboxContainer">
            <div class="checkboxRow">
            {#each dissatisfied_generated_image.slice(0, Math.ceil(dissatisfied_generated_image.length / 2)) as item (item.value)}
                <label class="checkboxLabel">
                <input
                    type="checkbox"
                    bind:group={selectedValues1}
                    value={item.value}
                /> {item.label}
                </label>
        {/each}
        </div>
    
    <div class="checkboxRow">
      {#each dissatisfied_generated_image.slice(Math.ceil(dissatisfied_generated_image.length / 2)) as item (item.value)}
        <label class="checkboxLabel">
          <input
            type="checkbox"
            bind:group={selectedValues1}
            value={item.value}
          /> {item.label}
        </label>
      {/each}
    </div>
  </div>
{/if}
        <br>
        <p class="question"> 4. 생성된 이미지를 기반하여 추가되면 좋을 듯한 기능 혹은 아이디어가 있으신가요?</p>
        <TextArea bind:value={image_add_function} />
        <br>

    </div>
    <div class= survey-container>
        <p class="question">5. 생성된 얼굴이 영상에 자연스럽게 적용되었다고 생각하시나요?</p>
        <Radio options={face_to_gif_well} fontSize={20} legend=''  bind:userSelected={f2g}/>
        <br>
        <p class="question"> 6. 더 다양한 영상이 추가되길 원하시나요?</p>
        <Radio options={more_based_gif} fontSize={20} legend=''  bind:userSelected={mbg} />
        <br>
        {#if mbg}

                <p class="question"> 6+. 합성의 기반이 될 영상을 추가한다면 어떤 종류를 원하시나요? (복수선택 가능)</p>
                <div style="display: flex; items-align:flex-start; gap: 15px; font-size: 15pt;">
                {#each gif_based_additional_function as item (item.value)}
                <label>
                    <input 
                        type="checkbox"
                        bind:group={selectedValues2}
                        value={item.value}
                    /> {item.label}
                </label><br>
                {/each}
                </div>
                <br>
            {/if}
            
    </div>
    <div class= survey-container>
        <p class="question">7. 현재 서비스 제공 소요시간은 약 2분 입니다. 해당 시간동안 로딩 화면에서 대기하실 의향이 있으신가요?</p>
        <Radio options={waiting_or_not} fontSize={20} legend=''  bind:userSelected={won}/> <br>
        {#if won}
<div class="question">7+. 대기하지 않기를 원하신다면 어떤 방향으로 서비스가 개선되기를 희망하시나요?</div>
<div class="checkboxContainer">
  <div class="checkboxRow">
    {#each waiting_about.slice(0, Math.ceil(waiting_about.length / 2)) as item}
      <label class="checkboxLabel">
        <input
          type="checkbox"
          bind:group={selectedValues3}
          value={item.value}
        /> {item.label}
      </label>
    {/each}
  </div>

  <div class="checkboxRow">
    {#each waiting_about.slice(Math.ceil(waiting_about.length / 2)) as item}
      <label class="checkboxLabel">
        <input
          type="checkbox"
          bind:group={selectedValues3}
          value={item.value}
        /> {item.label}
      </label>
    {/each}
  </div>
</div>
{/if}
    </div>
    <div class= survey-container>
        <p class="question">8. 이 서비스를 친구나 가족에게 추천할 의향이 있으신가요?</p>
        <Radio options={dissatified_service} fontSize={20}  legend='' bind:userSelected={service}/><br>
        <p class="question">9. 해당 서비스에 대한 건의사항이나 불편했던 점, 좋았던 점 등에 대해 자유롭게 작성해주세요</p>
        <TextArea bind:value={service_comments} /> <br>
    </div>
    <div class= survey-container style="align-items: center;"> 
        <div> 
            <p class= question >개인정보 수집 이용 동의서 (선택)</p>
            <p style="font-size: 15pt;"> - 추첨을 통한 기프티콘 제공을 위해 개인정보 수집 이용 동의를 받고 있습니다.</p>

        </div>
        <div
        style="
            overflow-y: auto;
            background: #ffffff;
            border-radius: 10px;
            border: 1px solid #000000;
            padding: 10px 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            align-items: flex-start;
            justify-content: flex-start;
            width: 70%;
            height: 30%;
            max-height: 350px;
            color: rgba(0, 0, 0, 0.87);
            text-align: left;
            font-family: 'DmSans-Medium', sans-serif;
            font-size: 20px;
            line-height: 23px;
            font-weight: 500;
            margin: 2px;
        "
        >
        
        <p><strong>1. 수집하는 개인정보의 항목:</strong></p>
        <ul>
            <li>- 이메일</li>
        </ul>
        <p><strong>2. 개인정보의 수집 및 이용 목적:</strong></p>
        <ul>
            <li>- 설문조사 응답 결과 확인 및 통보</li>
            <li>- 응답자와의 연락 및 안내</li>
        </ul>
        <p><strong>3. 개인정보의 보유 및 이용 기간:</strong></p>
        <ul>개인정보 수집 및 이용 목적 달성 후 즉시 파기합니다.</ul>
        <p><strong>4. 동의 거부 권리:</strong></p>

        <p>본인은 개인정보 제공에 대한 동의를 거부할 권리가 있습니다. <br>
            단, 동의를 거부할 경우 설문조사 경품 추첨에 제한이 있음을 인지합니다.  </p>
    </div>
            <p class="question"> 본인은 위와 같이 개인정보 수집 및 이용에 동의 합니다.</p>
            <Radio options={agree} fontSize={20} legend='' bind:userSelected={agree2} />
        {#if agree2} 
            <p class="question"> 이메일 입력</p>
            <input class="t_box" style="width: 50%;"type="text" placeholder='makezenerator@gmail.com' bind:value={email} />
        {/if}
        <br>
        

        <button type="submit"
    style="{'background: var(--neutral-10, #000000);border-radius: 50px; border-style: solid; border-color: var(--neutral-10, #486284); border-width: 1px; padding: 12px 20px 12px 20px; display: flex; flex-direction: row; gap: 10px; align-items: center; justify-content: center; position: relative; overflow: hidden;' + style}"
    >

    
    <div
     
      style="
        color: var(--neutral-0, #ffffff);
        text-align: left;
        font-family: var(--body-small-font-family, 'DmSans-Regular', sans-serif);
        font-size: var(--body-small-font-size, 24px);
        line-height: var(--body-small-line-height, 24px);
        font-weight: var(--body-small-font-weight, 400);
        position: relative;
      "
    >
      제출하기
    </div>
    </button>
    </div>
</form>

