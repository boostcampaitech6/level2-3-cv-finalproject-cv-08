<script>
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();
  export let variant = 'variant-3';
  let className = '';
  export { className as class };
  const variantsClassName = 'default-' + variant;
  
  let mediaRecorder;
  let audioChunks = [];
  let isRecordingComplete = false; 
  let progress = 0;

  async function startRecording() {
    audioChunks = []; 
    isRecordingComplete = false; 

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      
      mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
      };
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);

        dispatch('audioRecorded', audioUrl );
        dispatch('blobUpdated', audioBlob);
        isRecordingComplete = true;
      };

      setTimeout(() => {
        mediaRecorder.start();
        progress = 100;
        dispatch('progressUpdated', progress);

        setTimeout(() => {
          mediaRecorder.stop();
        }, 10100); 
      }, 1000);
      
    } catch (err) {
      console.error('오디오 입력을 시작하는데 실패했습니다:', err);
    }
  }

  function restartRecording() {
    audioChunks = []; 
    isRecordingComplete = false; 
    dispatch('audioRecorded', "");
    dispatch('progressUpdated',0);
  }
</script>

<div style="{'width: 100px; height: 50px; position: relative; '}">
  {#if !isRecordingComplete}
    <img
      class="{'frame-6 ' + className + ' ' + variantsClassName}"
      style="..."
      src="/join/frame-60.svg"
      on:click={startRecording}
      alt="audio record"
    />
  {:else}
    <img
      class="{'frame-6 ' + className + ' ' + variantsClassName}"
      style="..."
      src="/join/restart.png"
      on:click={restartRecording}
      alt="restart"
    />
  {/if}
</div>
