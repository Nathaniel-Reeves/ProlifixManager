<template>
  <div class="mb-3 wide">
    <v-select
      :id="id"
      :options="paginated"
      label="process_name"
      v-model="selected_process"
      :loading="!processes_loaded"
      :placeholder="!processes_loaded ? 'Loading...':'Choose Manufacturing Process...'"
      aria-describedby="select_process-live-feedback"
      :class="[((selected_process !== null && selected_process.process_id > 0) || !processReq ? '' : 'is-invalid'), 'wide']"
      :disabled="(selected_process !== null && selected_process.process_id > 0) || disabled"
      :clearable="false"
      :filterable="false"
      @open="onOpen"
      @close="onClose"
      @search="(query) => (search = query)"
      >
      <template #option="{ process_id, process_name }">
        <div style="display:flex; flex-direction: row; align-items: center; min-height: 60px;">
          <b-button v-on:click.stop class="mr-2" variant="light" :to="'/manufacturing/process/'+process_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
          <div>{{ process_name }}</div>
        </div>
      </template>
      <template #list-footer>
        <li v-show="hasNextPage" ref="load" class="loader">
          Loading more options...
        </li>
      </template>
    </v-select>
    <div id="select_process-live-feedback" class="invalid-feedback">This is a required field.</div>
    <!-- <b-tooltip v-if="selected_process !== null && selected_process.process_id > 0 && initial" :target="id" triggers="hover">{{ selected_process.process_name }}</b-tooltip> -->
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
  name: 'ChooseProcess',
  components: {
    vSelect
  },
  props: {
    processes: {
      type: Array,
      required: true
    },
    selected: {
      type: Object,
      default: null
    },
    processReq: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      selected_process: null,
      id: Math.floor(Math.random() * 100000),
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
    selected_process: function (val) {
      this.$emit('process', val)
    }
  },
  mounted () {
    this.observer = new IntersectionObserver(this.infiniteScroll)
  },
  computed: {
    processes_loaded: function () {
      return this.processes.length > 0
    },
    filtered () {
      if (this.search === '') {
        return this.processes
      }
      if (this.processes.length === 0) {
        return []
      }
      return this.processes.filter((process) => process.process_name.toLowerCase()?.includes(this.search.toLowerCase()))
    },
    paginated () {
      return this.filtered.slice(0, this.limit)
    },
    hasNextPage () {
      return this.paginated.length < this.filtered.length
    }
  },
  created: function () {
    this.selected_process = this.selected != null ? this.selected : null
  }
}
</script>
