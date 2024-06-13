<template>
  <div class="mb-3">
    <v-select :options="organizations" label="organization_initial" v-model="selected_org" :loading="!orgs_loaded" :clearable="selected_org != null" :placeholder="!orgs_loaded ? 'Loading...':'Choose...'" style="width: 150px;">
      <template #option="{ organization_name, organization_initial }">
        <div>{{ organization_name }} | {{ organization_initial }}</div>
      </template>
    </v-select>
  </div>
</template>

<style>
.vs__dropdown-menu {
  width: 600px;
  max-height: 300px;
  overflow-y: auto;
}
</style>

<script>
import vSelect from 'vue-select'

export default {
  name: 'ChooseOrg',
  components: {
    vSelect
  },
  props: [
    'organizations',
    'selected'
  ],
  data: function () {
    return {
      selected_org: null
    }
  },
  methods: {
  },
  watch: {
    selected_org: function (val) {
      this.$emit('org', val)
    }
  },
  computed: {
    orgs_loaded: function () {
      return this.organizations.length > 0
    },
    ing_array: function () {
      if (Array.isArray(this.organizations) && this.organizations.length > 0) {
        return this.organizations
      }
      return []
    }
  },
  created: function () {
    this.selected_org = this.selected != null ? this.selected : null
  }
}
</script>
