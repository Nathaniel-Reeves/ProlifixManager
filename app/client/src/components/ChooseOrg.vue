<template>
  <div class="mb-3">
    <v-select
      :id="id"
      :options="organizations"
      label="organization_initial"
      v-model="selected_org"
      :loading="!orgs_loaded"
      :clearable="selected_org != null"
      :placeholder="!orgs_loaded ? 'Loading...':'Choose...'"
      style="width: 150px;"
      aria-describedby="select_org-live-feedback"
      :class="(selected_org !== null || !orgReq ? '' : 'is-invalid')"
    >
      <template #option="{ organization_id, organization_name, organization_initial }">
        <div style="display:flex; flex-direction: row; align-items: center; min-height: 60px;">
          <b-button v-on:click.stop class="mr-2" variant="light" :to="'/organizations/'+organization_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
          <div>{{ organization_name }} | {{ organization_initial }}</div>
        </div>
      </template>
    </v-select>
    <div id="select_org-live-feedback" class="invalid-feedback">This is a required field.</div>
    <b-tooltip v-if="selected_org != null && selected_org.organization_id != 0" :target="id" triggers="hover">{{ selected_org.organization_name }}</b-tooltip>
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
    'selected',
    'orgReq'
  ],
  data: function () {
    return {
      selected_org: null,
      id: Math.floor(Math.random() * 100000) + '-org-name'
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
