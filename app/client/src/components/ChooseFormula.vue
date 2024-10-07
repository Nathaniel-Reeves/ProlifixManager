<template>
  <div class="mb-3 wide">
    <v-select
      :id="id"
      :options="paginated"
      label="formulation_version"
      v-model="selected_formula"
      :loading="!formulas_loaded"
      :placeholder="placeholder"
      aria-describedby="select_formula-live-feedback"
      :class="[((selected_formula !== null && selected_formula.formula_id > 0) || !formulaReq ? '' : 'is-invalid'), 'wide']"
      :disabled="(selected_formula !== null && selected_formula.formula_id > 0) || disabled"
      :clearable="false"
      :filterable="false"
      @open="onOpen"
      @close="onClose"
      @search="(query) => (search = query)"
      >
      <template #option="{ formulation_version }">
        <div style="display:flex; flex-direction: row; align-items: center; min-height: 40px;">
          <div>V{{ formulation_version }}</div>
        </div>
      </template>
      <template #list-footer>
        <li v-show="hasNextPage" ref="load" class="loader">
          Loading more options...
        </li>
      </template>
    </v-select>
    <div id="select_formula-live-feedback" class="invalid-feedback">This is a required field.</div>
    <!-- <b-tooltip v-if="selected_formula !== null && selected_formula.process_id > 0 && initial" :target="id" triggers="hover">{{ selected_formula.formulation_version }}</b-tooltip> -->
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
  width: 100%;
}
</style>

<script>
import vSelect from 'vue-select'

export default {
  name: 'ChooseFormula',
  components: {
    vSelect
  },
  props: {
    formulas: {
      type: Array,
      required: true
    },
    selected: {
      type: Object,
      default: null
    },
    formulaReq: {
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
      selected_formula: null,
      id: Math.floor(Math.random() * 100000),
      observer: null,
      limit: 10,
      search: '',
      placeholder: 'Loading...'
    }
  },
  methods: {
    calPlaceholder: function () {
      if (this.formulas_loaded) {
        this.placeholder = 'Choose Product Formula...'
      }
      setTimeout(() => {
        if (!this.formulas_loaded || this.formulas.length === 0) {
          this.placeholder = 'No formulas Available, Make a New Formula.'
        }
      }, 1500)
    },
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
    selected_formula: function (val) {
      this.$emit('formula', val)
    }
  },
  mounted () {
    this.observer = new IntersectionObserver(this.infiniteScroll)
  },
  computed: {
    formulas_loaded: function () {
      return this.formulas.length > 0
    },
    filtered () {
      if (this.search === '') {
        return this.formulas
      }
      if (this.formulas.length === 0) {
        return []
      }
      return this.formulas.filter((formula) => formula.formulation_version.toLowerCase()?.includes(this.search.toLowerCase()))
    },
    paginated () {
      return this.filtered.slice(0, this.limit)
    },
    hasNextPage () {
      return this.paginated.length < this.filtered.length
    }
  },
  created: function () {
    this.selected_formula = this.selected != null ? this.selected : null
    this.calPlaceholder()
  }
}
</script>
