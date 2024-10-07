<template>
  <div class="mb-3 wide">
    <b-row align-v="center">
      <b-col style="width: 40%;">
        <v-select
          :id="id"
          :options="paginated"
          label="product_name"
          v-model="selected_product"
          :loading="!products_loaded"
          :placeholder="placeholder"
          aria-describedby="select_product-live-feedback"
          :class="[((selected_product !== null && selected_product.product_id > 0) || !variantReq ? '' : 'is-invalid'), 'wide']"
          :disabled="(selected_product !== null && selected_product.product_id > 0) || disabled"
          :clearable="false"
          :filterable="false"
          @open="onOpen"
          @close="onClose"
          @search="(query) => (search = query)"
          >
          <template #option="{ product_id, product_name, certified_fda, certified_gluten_free, certified_gmp, certified_halal, certified_kosher, certified_made_with_organic, certified_national_sanitation_foundation, certified_non_gmo, certified_us_pharmacopeia, certified_usda_organic, certified_vegan, certified_wildcrafted }">
            <div style="display:flex; flex-direction: row; align-items: center; min-height: 40px;">
              <b-button v-on:click.stop class="mr-2" variant="light" :to="'/catalogue/products/'+product_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
              <div>{{ product_name }}</div>
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
        <div id="select_product-live-feedback" class="invalid-feedback">This is a required field.</div>
      </b-col>
      <b-col style="width: 60%;">
        <CertBadge :data="selected_product"></CertBadge>
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
    products: {
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
      selected_product: null,
      id: Math.floor(Math.random() * 100000),
      observer: null,
      limit: 10,
      search: '',
      placeholder: 'Loading...'
    }
  },
  methods: {
    calPlaceholder: function () {
      if (this.products_loaded) {
        this.placeholder = 'Choose Product...'
      }
      setTimeout(() => {
        if (!this.products_loaded || this.products.length === 0) {
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
    selected_product: function (val) {
      this.$emit('product', val)
    }
  },
  mounted () {
    this.observer = new IntersectionObserver(this.infiniteScroll)
  },
  computed: {
    products_loaded: function () {
      return this.products.length > 0
    },
    filtered () {
      if (this.search === '') {
        return this.products
      }
      if (this.products.length === 0) {
        return []
      }
      return this.products.filter((product) => product.product_name.toLowerCase()?.includes(this.search.toLowerCase()) && product.current_product)
    },
    paginated () {
      return this.filtered.slice(0, this.limit)
    },
    hasNextPage () {
      return this.paginated.length < this.filtered.length
    }
  },
  created: function () {
    this.selected_product = this.selected != null ? this.selected : null
    this.calPlaceholder()
  }
}
</script>
