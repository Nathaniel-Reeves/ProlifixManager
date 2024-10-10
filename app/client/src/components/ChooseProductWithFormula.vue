<template>
  <div class="mb-3 wide">
    <b-row align-v="center">
      <b-col style="width: 40%;">
        <v-select
          :id="id"
          :options="paginated"
          label="title"
          v-model="selected_product_with_formula"
          :loading="!productsWithFormulasLoaded"
          :placeholder="placeholder"
          aria-describedby="select_product_with_formula-live-feedback"
          :class="[((selected_product_with_formula !== null && selected_product_with_formula.product_id > 0) || !variantReq ? '' : 'is-invalid'), 'wide']"
          :disabled="(selected_product_with_formula !== null && selected_product_with_formula.product_id > 0) || disabled"
          :clearable="false"
          :filterable="false"
          @open="onOpen"
          @close="onClose"
          @search="(query) => (search = query)"
          >
          <template #option="{ product_id, title, product }">
            <div style="display:flex; flex-direction: row; align-items: center; min-height: 40px;">
              <b-button v-on:click.stop class="mr-2" variant="light" :to="'/catalogue/products/'+product_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
              <div>{{ title }}</div>
              <CertBadge :data="product"></CertBadge>
            </div>
          </template>
          <template #list-footer>
            <li v-show="hasNextPage" ref="load" class="loader">
              Loading more options...
            </li>
          </template>
        </v-select>
        <div id="select_product_with_formula-live-feedback" class="invalid-feedback">This is a required field.</div>
      </b-col>
      <b-col style="width: 60%;">
        <CertBadge :data="selected_product_with_formula.product"></CertBadge>
      </b-col>
    </b-row>
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
import CertBadge from './CertBadge.vue'
import vSelect from 'vue-select'

export default {
  name: 'ChooseProduct',
  components: {
    CertBadge,
    vSelect
  },
  props: {
    productsWithFormulas: {
      type: Array,
      required: true
    },
    selected: {
      type: Object,
      default: null
    },
    productReq: {
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
      selected_product_with_formula: null,
      id: Math.floor(Math.random() * 100000),
      observer: null,
      limit: 10,
      search: '',
      placeholder: 'Loading...'
    }
  },
  methods: {
    calPlaceholder: function () {
      if (this.productsWithFormulasLoaded) {
        this.placeholder = 'Choose Product...'
      }
      setTimeout(() => {
        if (!this.productsWithFormulasLoaded || this.productsWithFormulas.length === 0) {
          this.placeholder = 'No Products Available, Make a New Product.'
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
    selected_product_with_formula: function (val) {
      this.$emit('productWithFormula', val)
    }
  },
  mounted () {
    this.observer = new IntersectionObserver(this.infiniteScroll)
  },
  computed: {
    productsWithFormulasLoaded: function () {
      return this.productsWithFormulas.length > 0
    },
    filtered () {
      if (this.search === '') {
        return this.productsWithFormulas
      }
      if (this.productsWithFormulas.length === 0) {
        return []
      }
      return this.productsWithFormulas.filter((productwformula) => productwformula.title.toLowerCase()?.includes(this.search.toLowerCase()))
    },
    paginated () {
      return this.filtered.slice(0, this.limit)
    },
    hasNextPage () {
      return this.paginated.length < this.filtered.length
    }
  },
  created: function () {
    this.selected_product_with_formula = this.selected != null ? this.selected : null
    this.calPlaceholder()
  }
}
</script>
