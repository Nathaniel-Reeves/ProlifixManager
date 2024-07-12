<template>
  <div class="mb-3" :class="(initial ? 'initial' : 'wide')">
    <v-select
      :id="id"
      :options="paginated"
      :label="initial ? 'organization_primary_initial' : 'organization_primary_name'"
      v-model="selected_org"
      :loading="!orgs_loaded"
      :placeholder="!orgs_loaded ? 'Loading...':'Choose...'"
      aria-describedby="select_org-live-feedback"
      :class="[((selected_org !== null && selected_org.organization_id > 0) || !orgReq ? '' : 'is-invalid'), (initial ? 'initial' : 'wide')]"
      :disabled="selected_org !== null && selected_org.organization_id > 0 && initial"
      :clearable="false"
      :filterable="false"
      @open="onOpen"
      @close="onClose"
      @search="(query) => (search = query)"
      >
      <template #option="{ organization_id, organization_primary_name, organization_primary_initial }">
        <div style="display:flex; flex-direction: row; align-items: center; min-height: 60px;">
          <b-button v-on:click.stop class="mr-2" variant="light" :to="'/organizations/'+organization_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
          <div>{{ organization_primary_name }} | {{ organization_primary_initial }}</div>
        </div>
      </template>
      <template #list-footer>
        <li v-show="hasNextPage" ref="load" class="loader">
          Loading more options...
        </li>
      </template>
    </v-select>
    <div id="select_org-live-feedback" class="invalid-feedback">This is a required field.</div>
    <b-tooltip v-if="selected_org !== null && selected_org.organization_id > 0 && initial" :target="id" triggers="hover">{{ selected_org.organization_primary_name }}</b-tooltip>
  </div>
</template>

<style scoped>
.vs__dropdown-menu {
  width: 600px;
  max-height: 300px;
  overflow-y: auto;
}

.loader {
  text-align: center;
  color: #bbbbbb;
}
.initial {
  width: 150px;
}
.wide {
  width: 81%;
}
</style>

<script>
import vSelect from 'vue-select'

export default {
  name: 'ChooseOrg',
  components: {
    vSelect
  },
  props: {
    organizations: {
      type: Array,
      required: true
    },
    selected: {
      type: Object,
      default: null
    },
    orgReq: {
      type: Boolean,
      default: false
    },
    initial: {
      type: Boolean,
      default: true
    }
  },
  data: function () {
    return {
      selected_org: null,
      id: Math.floor(Math.random() * 100000) + '-org-name',
      observer: null,
      limit: 10,
      search: ''
    }
  },
  methods: {
    async onOpen () {
      if (this.hasNextPage) {
        await this.$nextTick()
        this.observer.observe(this.$refs.load)
      }
    },
    onClose () {
      this.observer.disconnect()
    },
    async infiniteScroll ([{ isIntersecting, target }]) {
      if (isIntersecting) {
        const ul = target.offsetParent
        const scrollTop = target.offsetParent.scrollTop
        this.limit += 10
        await this.$nextTick()
        ul.scrollTop = scrollTop
      }
    }
  },
  watch: {
    selected_org: function (val) {
      this.$emit('org', val)
    }
  },
  mounted () {
    this.observer = new IntersectionObserver(this.infiniteScroll)
  },
  computed: {
    orgs_loaded: function () {
      return this.organizations.length > 0
    },
    filtered () {
      return this.organizations.filter((org) => (org.organization_primary_name?.includes(this.search) || org.organization_primary_initial?.includes(this.search)))
    },
    paginated () {
      return this.filtered.slice(0, this.limit)
    },
    hasNextPage () {
      return this.paginated.length < this.filtered.length
    }
  },
  created: function () {
    this.selected_org = this.selected != null ? this.selected : null
  }
}
</script>
