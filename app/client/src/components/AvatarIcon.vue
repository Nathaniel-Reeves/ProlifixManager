<template>
  <div>
    <div v-if="logged_in">
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
  computed: {
    logged_in: function () {
      return this.$root.userData.user_id
    },
    initials: function () {
      if (this.logged_in) {
        const f = Array.from(this.$root.userData.first_name)[0]
        const l = Array.from(this.$root.userData.last_name)[0]
        const i = f + l
        return i
      } else {
        return ''
      }
    }
  }
}
</script>
