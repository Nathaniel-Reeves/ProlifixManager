<template>
  <div>
    <b-row align-v="center">
      <b-col :class="[noCerts ? 'width-100' : 'width-80']">
        <v-select
          :options="paginated"
          label="component_primary_name"
          v-model="selected_component"
          :loading="!components_loaded"
          :placeholder="!components_loaded ? 'Loading...':'Choose...'"
          aria-describedby="select_component-live-feedback"
          :class="(!compReq || selected_component !== null && selected_component.component_id > 0 ? '' : 'is-invalid')"
          :disabled="selected_component !== null && selected_component?.component_id > 0 && disableAfterEntry"
          :clearable="!disableAfterEntry"
          @open="onOpen"
          @close="onClose"
          @search="(query) => (search = query)"
          :append-to-body="true"
        >
          <template #option="{ component_id, component_primary_name, certified_fda, certified_gluten_free, certified_gmp, certified_halal, certified_kosher, certified_made_with_organic, certified_national_sanitation_foundation, certified_non_gmo, certified_us_pharmacopeia, certified_usda_organic, certified_vegan, certified_wildcrafted }">
            <div style="display:flex; flex-direction: row; align-items: center; min-height: 60px;">
              <b-button v-on:click.stop class="mr-2" variant="light" :to="'/catalogue/components/'+component_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
              <div style="min-width: 200px;">{{ component_primary_name }}</div>
              <CertBadge :data="{
                'certified_fda': certified_fda,
                'certified_gluten_free': certified_gluten_free,
                'certified_gmp': certified_gmp,
                'certified_halal': certified_halal,
                'certified_kosher': certified_kosher,
                'certified_made_with_organic': certified_made_with_organic,
                'certified_national_sanitation_foundation': certified_national_sanitation_foundation,
                'certified_non_gmo': certified_non_gmo,
                'certified_us_pharmacopeia': certified_us_pharmacopeia,
                'certified_usda_organic': certified_usda_organic,
                'certified_vegan': certified_vegan,
                'certified_wildcrafted': certified_wildcrafted
              }"></CertBadge>
            </div>
          </template>
          <template #list-footer>
            <li v-show="hasNextPage" ref="load" class="loader">
              Loading more options...
            </li>
          </template>
        </v-select>
        <div id="select_component-live-feedback" class="invalid-feedback">This is a required field.</div>
      </b-col>
      <b-col v-if="!noCerts" style="max-width: 20%;">
        <CertBadge :data="selected_component"></CertBadge>
      </b-col>
    </b-row>
  </div>
</template>

<style>
.width-100 {
  width: 100%;
}
.width-80 {
  width: 80%;
}
.v-select.drop-up.vs--open .vs__dropdown-toggle {
  border-radius: 0 0 4px 4px;
  border-top-color: transparent;
  border-bottom-color: rgba(60, 60, 60, 0.26);
}

[data-popper-placement='top'] {
  border-radius: 4px 4px 0 0;
  border-top-style: solid;
  border-bottom-style: none;
  box-shadow: 0 -3px 6px rgba(0, 0, 0, 0.15);
}

.vs__dropdown-menu {
  width: 600px;
  max-height: 300px;
  overflow-y: auto;
}

.loader {
  text-align: center;
  color: #bbbbbb;
}
</style>

<script>
import CertBadge from './CertBadge.vue'
import vSelect from 'vue-select'

export default {
  name: 'ChooseComponent',
  components: {
    CertBadge,
    vSelect
  },
  props: {
    widthRatio: {
      type: String,
      default: '80'
    },
    components: {
      type: Array,
      required: true
    },
    selected: {
      type: Object,
      default: null
    },
    noCerts: {
      type: Boolean,
      default: false
    },
    compReq: {
      type: Boolean,
      default: false
    },
    disableAfterEntry: {
      type: Boolean,
      default: true
    }
  },
  data: function () {
    return {
      selected_component: null,
      observer: null,
      limit: 10,
      search: '',
      placement: 'top'
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
    selected_component: function (val) {
      this.$emit('comp', val)
    }
  },
  mounted () {
    this.observer = new IntersectionObserver(this.infiniteScroll)

    this.selected_component = this.selected !== null ? this.selected : null
    if (this.selected !== null && this.selected.component_name) {
      this.selected_component.component_primary_name = this.selected.component_name
    }
  },
  computed: {
    components_loaded: function () {
      return this.components.length > 0
    },
    filtered () {
      if (this.search === '') {
        return this.components
      }
      if (this.components.length === 0) {
        return []
      }
      return this.components.filter((comp) => comp.component_primary_name ? comp.component_primary_name.toLowerCase()?.includes(this.search.toLowerCase()) : false)
    },
    paginated () {
      return this.filtered.slice(0, this.limit)
    },
    hasNextPage () {
      return this.paginated.length < this.filtered.length
    }
  },
  created: function () {
    this.selected_component = this.selected !== null ? this.selected : null
    if (this.selected !== null && this.selected.component_name) {
      this.selected_component.component_primary_name = this.selected.component_name
    }
  }
}
</script>
