<template>
  <div class="home">
    <div class="card m-2 p-3" style="max-width: 30rem;">
      <img class="card-img-top" style="max-width: 20rem; align-self:center;" alt="Vue logo" src="../assets/Company Images/Prolifix Logo Cropped.jpg">
      <HelloWorld msg="Welcome to Your Vue.js App"/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>
