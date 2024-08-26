<template>
  <div class="mb-3 wide">
    <v-select
      :id="id"
      :options="paginated"
      label="variant_title"
      v-model="selected_variant"
      :loading="!variants_loaded"
      :placeholder="placeholder"
      aria-describedby="select_variant-live-feedback"
      :class="[((selected_variant !== null && selected_variant.variant_id > 0) || !variantReq ? '' : 'is-invalid'), 'wide']"
      :disabled="(selected_variant !== null && selected_variant.variant_id > 0) || disabled"
      :clearable="false"
      :filterable="false"
      @open="onOpen"
      @close="onClose"
      @search="(query) => (search = query)"
      >
      <template #option="{ variant_title, variant_type }">
        <div style="display:flex; flex-direction: row; align-items: center; min-height: 40px;">
          <div>{{ variant_type.charAt(0).toUpperCase() + variant_type.slice(1) + ' Fill' }} - {{ variant_title }}</div>
        </div>
      </template>
      <template #list-footer>
        <li v-show="hasNextPage" ref="load" class="loader">
          Loading more options...
        </li>
      </template>
    </v-select>
    <div id="select_variant-live-feedback" class="invalid-feedback">This is a required field.</div>
    <!-- <b-tooltip v-if="selected_variant !== null && selected_variant.process_id > 0 && initial" :target="id" triggers="hover">{{ selected_variant.variant_title }}</b-tooltip> -->
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
  name: 'ChooseVariant',
  components: {
    vSelect
  },
  props: {
    variants: {
      type: Array,
      required: true
    },
    selected: {
      type: Object,
      default: null
    },
    variantReq: {
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
      selected_variant: null,
      id: Math.floor(Math.random() * 100000),
      observer: null,
      limit: 10,
      search: '',
      placeholder: 'Loading...'
    }
  },
  methods: {
    calPlaceholder: function () {
      if (this.variants_loaded) {
        this.placeholder = 'Choose Product Variant...'
      }
      setTimeout(() => {
        if (!this.variants_loaded || this.variants.length === 0) {
          this.placeholder = 'No Variants Available, Make a New Variant.'
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
    selected_variant: function (val) {
      this.$emit('variant', val)
    }
  },
  mounted () {
    this.observer = new IntersectionObserver(this.infiniteScroll)
  },
  computed: {
    variants_loaded: function () {
      return this.variants.length > 0
    },
    filtered () {
      if (this.search === '') {
        return this.variants
      }
      if (this.variants.length === 0) {
        return []
      }
      return this.variants.filter((variant) => variant.variant_title.toLowerCase()?.includes(this.search.toLowerCase()) && !variant.discontinued)
    },
    paginated () {
      return this.filtered.slice(0, this.limit)
    },
    hasNextPage () {
      return this.paginated.length < this.filtered.length
    }
  },
  created: function () {
    this.selected_variant = this.selected != null ? this.selected : null
    this.calPlaceholder()
  }
}
</script>
