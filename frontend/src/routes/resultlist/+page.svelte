<script>
  import MovingFilled from "../../components/button/moving_filled.svelte";
  import Header from "../../components/header/header_login.svelte";
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell} from 'flowbite-svelte';

  let items = [];

  async function fetchData() {
    const token = sessionStorage.getItem('auth_token'); 
    const response = await fetch('https://api.makezenerator.com/api/v1/mz-request', {
      method: 'GET',
      headers: {
        'Token': token,
      },
    });

    if (response.ok) {
      const data = await response.json();
      items = data.mz_request_list; 
    } else if(response.status === 400) {
      alert("데이터베이스 에러");
    } else if(response.status === 401) {
      alert(`세션이 만료되었습니다. \n다시 로그인 해주세요`);
      goto("/");
      return
    }
    else {
      console.error('데이터를 가져오는 데 실패했습니다.');
      alert("요청 중 에러가 발생했습니다.");
    }
  }

  onMount(() => {

    fetchData(); 
    const interval = setInterval(fetchData, 5000); 

    return () => {
      clearInterval(interval); 
    };
  });
  </script>



<div
style="{'background: var(--neutral-0, #ffffff);padding: 0px 0px 120px 0px; display: flex; flex-direction: column; gap: 70px; align-items: center; justify-content: flex-start; min-height: 100vh; position: relative ' }"
>
<Header />
<div>
  <img
    class="image-22"
    style="
      flex-shrink: 0;
      width: 166px;

      position: relative;
      object-fit: cover;
      margin-left: auto;
      margin-right: auto;
    "
    src="./logo/logo1.png"
    alt="logo"
  />
  <div
    style="
      color: #8c8686;
      text-align: center;
      font-family: var(--body-large-font-family, 'DmSans-Regular', sans-serif);
      font-size: var(--body-large-font-size, 20px);
      line-height: var(--body-large-line-height, 32px);
      font-weight: var(--body-large-font-weight, 400);
      position: relative;
      width: 612px;
      margin-left: auto;
      margin-right: auto;
    "
  > 
  <br>
    생성 이미지는 선택 버튼을 통해 확인하실 수 있습니다.
  </div>
</div>

  <Table hoverable={true}
    style="
        flex-shrink: 0;
        width: 1400px;
        font-size: 14pt;
    ">
    <TableHead>
      <TableHeadCell style="width: 15%; font-size:14pt;">요청 시간</TableHeadCell>
      <TableHeadCell style="width: 15%; font-size:14pt;">완료 시간</TableHeadCell>
      <TableHeadCell style="width: 8%; font-size:14pt;">성별</TableHeadCell>
      <TableHeadCell style="width: 8%; font-size:14pt;">나이</TableHeadCell>
      <TableHeadCell style="width: 10%; font-size:14pt;">진행 상태</TableHeadCell>
      <TableHeadCell style="font-size:14pt;">목소리 듣기</TableHeadCell>
      <TableHeadCell style="font-size:14pt;">결과 보기</TableHeadCell>
    </TableHead>
    <TableBody >
      {#each items as item}
        <TableBodyRow>
          <TableBodyCell>{item.created_at.replace('T', ' ')}</TableBodyCell>
          <TableBodyCell>
            {#if item.ata != null} {item.ata.replace('T', ' ')}{/if}
          </TableBodyCell>
          <TableBodyCell>{#if item.gender == "man" } 남성 {:else } 여성 {/if} </TableBodyCell>
          <TableBodyCell>{item.age}</TableBodyCell>

          <TableBodyCell>
            {#if item.status == "Proceeding"}<img src = "/resultlist/생성중.png" style="width: 100%; height: 100%; max-width: 100%; max-height: 100%; " alt="생성 중"/>
            {:else if item.status == "Success"}<img src = "/resultlist/생성완료.png" style="width: 100%; height: 100%; max-width: 100%; max-height: 100%;" alt="생성 완료"/>
            {:else} <img src = "/resultlist/생성실패.png "style="width: 100%; height: 45%; max-width: 100%; max-height: 100%;" alt="생성 실패"/>
            {/if}
          </TableBodyCell>
          <TableBodyCell>
              <audio src={item.voice_url} controls></audio>
            </TableBodyCell>
          <TableBodyCell>
            {#if item.status =="Success"}
              <MovingFilled targetPath='/result' name="결과 확인" id = {item.id} latest_id = {item.latest_mz_result_id} gender={item.gender}> </MovingFilled>
            <!-- {:else if item.status == "Failed"} -->
              {/if}
            </TableBodyCell>
        </TableBodyRow>
          {/each}
    </TableBody>
  </Table>
</div>


