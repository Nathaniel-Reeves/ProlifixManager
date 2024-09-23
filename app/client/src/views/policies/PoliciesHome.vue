<template>
  <div class="my_component">
    <TipTap v-model="content" :edit="edit" />
  </div>
</template>

<script>
import TipTap from '@/components/TipTap.vue'

export default {
  name: 'PoliciesHome',
  components: {
    TipTap
  },
  data: function () {
    return {
      loaded: true,
      edit: false,
      content: ''
    }
  },
  computed: {
    filterActive: function () {
      if (this.search_query.length > 0) {
        return true
      }
      return false
    }
  },
  methods: {
    info: function (item, index, button) {
      this.infoModal.title = `Row index: ${index}`
      this.infoModal.content = JSON.stringify(item, null, 2)
      this.$root.$emit('bv::show::modal', this.infoModal.id, button)
    },
    resetInfoModal: function () {
      this.infoModal.title = ''
      this.infoModal.content = ''
    },
    clearSearch: function () {
      this.search_query = ''
      this.search_query_buff = ''
    },
    search: function () {
      this.search_query = this.search_query_buff
    },
    handleVisible: function (isVisible) {
      this.isMd = isVisible
    }
  }
}
</script>

<style scoped>
.my_component {
  width: 90%;
}
@media (max-width: 1024px) {
  .my_component {
    width: 98%;
  }
}
@media (max-width: 400px) {
  .my_component {
    width: 100%;
  }
}
</style>
