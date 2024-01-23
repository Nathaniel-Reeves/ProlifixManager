<template>
  <div>
    <div v-show="!loggedInState">
      <b-avatar icon="person-circle" size="2.5rem"></b-avatar>
    </div>
    <div v-show="loggedInState">
      <b-avatar variant="success" :text="initials" size="2.5rem"></b-avatar>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AvatarIcon',
  props: {
    userData: Object,
    loggedInState: Boolean
  },
  data () {
    return {
      avatar_data: this.userData
    }
  },
  computed: {
    initials: function () {
      console.log(this.avatar_data)
      if (this.loggedInState) {
        const f = Array.from(this.avatar_data.first_name)[0]
        const l = Array.from(this.avatar_data.last_name)[0]
        const i = f + l
        return i
      } else {
        return ''
      }
    }
  }
}
</script>
