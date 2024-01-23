<template>
  <div>
    <div v-if="logged_in_state">
      <b-avatar variant="success" :text="initials" size="2.5rem"></b-avatar>
    </div>
    <div v-else>
      <b-avatar icon="person-circle" size="2.5rem"></b-avatar>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AvatarIcon',
  data () {
    return {
    }
  },
  props: {
    user_data: Object,
    logged_in_state: Boolean
  },
  computed: {
    initials: function () {
      console.log('generate avatar', this.user_data)
      console.log('login status', this.logged_in_state)
      if (this.logged_in_state) {
        const f = Array.from(this.user_data.first_name)[0]
        const l = Array.from(this.user_data.last_name)[0]
        const i = f + l
        return i
      } else {
        return ''
      }
    }
  }
}
</script>
