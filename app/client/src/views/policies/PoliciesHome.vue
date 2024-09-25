<template>
  <div class="my_component">
    <div
      v-b-visible="handleVisible"
      class="position-fixed d-block d-lg-none"
      style="z-index: 20000; height: 1px;"
    ></div>
    <div>
      <b-sidebar id="sidebar-right" title="Table of Contents" :right="true" shadow :lazy="true" backdrop-variant="dark" :no-close-on-route-change="true">
        <b-navbar v-b-scrollspy style="width: 100%;">
          <b-nav pills vertical class="accordion" style="width: 100%;">
            <b-nav-item href="#item-1" v-b-toggle.accordion-1>
                Item 1
            </b-nav-item>
            <b-nav pills>
              <b-collapse id="accordion-1" accordion="my-accordion" role="tabpanel">
                <b-nav-item class="ml-3 my-1" href="#item-1-1">Item 1-1</b-nav-item>
                <b-nav-item class="ml-3 my-1" href="#item-1-2">Item 1-2</b-nav-item>
              </b-collapse>
            </b-nav>
            <b-nav-item href="#item-2">Item 2</b-nav-item>
            <b-nav-item href="#item-3" v-b-toggle.accordion-3>Item 3</b-nav-item>
            <b-nav pills vertical>
              <b-collapse id="accordion-3" accordion="my-accordion" role="tabpanel">
                <b-nav-item class="ml-3 my-1" href="#item-3-1">Item 3-1</b-nav-item>
                <b-nav-item class="ml-3 my-1" href="#item-3-2">Item 3-2</b-nav-item>
              </b-collapse>
            </b-nav>
          </b-nav>
        </b-navbar>
      </b-sidebar>
    </div>
    <b-container class="p-0 m-2" fluid style="max-width: 96%;">
      <b-row class="mx-2" cols="1" cols-lg="2">
        <b-col class="p-1 d-flex justify-content-end" lg="3" v-if="!isMd">
          <b-card class="position-fixed mr-2" style="width: 20%;">
            <b-card-title>Table of Contents</b-card-title>
            <b-card-body class="pl-0" style="width: 100%;">
              <b-navbar v-b-scrollspy style="width: 100%;">
                <b-nav pills vertical class="accordion" style="width: 100%;">
                  <b-nav-item href="#item-1" v-b-toggle.accordion-1>
                      Item 1
                  </b-nav-item>
                  <b-nav pills>
                    <b-collapse id="accordion-1" accordion="my-accordion" role="tabpanel">
                      <b-nav-item class="ml-3 my-1" href="#item-1-1">Item 1-1</b-nav-item>
                      <b-nav-item class="ml-3 my-1" href="#item-1-2">Item 1-2</b-nav-item>
                    </b-collapse>
                  </b-nav>
                  <b-nav-item href="#item-2">Item 2</b-nav-item>
                  <b-nav-item href="#item-3" v-b-toggle.accordion-3>Item 3</b-nav-item>
                  <b-nav pills vertical>
                    <b-collapse id="accordion-3" accordion="my-accordion" role="tabpanel">
                      <b-nav-item class="ml-3 my-1" href="#item-3-1">Item 3-1</b-nav-item>
                      <b-nav-item class="ml-3 my-1" href="#item-3-2">Item 3-2</b-nav-item>
                    </b-collapse>
                  </b-nav>
                </b-nav>
              </b-navbar>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col class="p-1 d-flex justify-content-start" lg="9">
          <b-card class="custom-content-card">
            <b-card-title class="input-group d-flex justify-content-between">
              <h2>TEMP</h2>
              <b-button v-if="isMd" v-b-tooltip.hover title="Table of Contents" v-b-toggle.sidebar-right style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light" type="button" id="button-addon2">
                <b-icon icon="list"></b-icon>
              </b-button>
            </b-card-title>
            <b-card-body>
              <div>
                <h4 id="item-1" style="">Item 1</h4>
                <p>{{ text }}</p>
                <h5 id="item-1-1" style="">Item 1-1</h5>
                <p>{{ text }}</p>
                <h5 id="item-1-2" style="">Item 2-2</h5>
                <p>{{ text }}</p>
                <h4 id="item-2" style="">Item 2</h4>
                <p>{{ text }}</p>
                <h4 id="item-3" style="">Item 3</h4>
                <p>{{ text }}</p>
                <h5 id="item-3-1" style="">Item 3-1</h5>
                <p>{{ text }}</p>
                <h5 id="item-3-2" style="">Item 3-2</h5>
                <p>{{ text }}</p>
              </div>
              <TipTap v-model="content" :edit="edit" />
            </b-card-body>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
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
      isMd: false,
      edit: false,
      content: '',
      text: `
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer pharetra vehicula est id vestibulum. Etiam aliquam, velit sed mattis cursus, lacus nisl ultrices neque, et tristique dui justo eu elit. Proin vehicula efficitur velit, et luctus ligula commodo vitae. Fusce fringilla urna in auctor gravida. Donec vitae fermentum eros. Quisque tempor purus et massa lacinia, vitae pharetra lectus aliquam. Aenean diam nisi, condimentum et nisl ut, sollicitudin suscipit turpis. Vivamus orci justo, fringilla ornare mi a, gravida congue quam. Vivamus non vulputate tortor, nec gravida risus. Nullam in dignissim dolor, in mollis eros. Phasellus at elit rutrum, venenatis nunc sed, vestibulum dui. Maecenas sit amet nulla et libero semper fringilla eu eget augue. Phasellus lobortis neque in lobortis luctus.

          Nam vehicula nibh at scelerisque egestas. Morbi a efficitur nibh, a bibendum elit. Nulla vehicula nulla arcu, et viverra elit elementum sit amet. Cras feugiat leo nisl, eu semper lectus tempus vel. Sed finibus nisl nisi, vel cursus lorem finibus eget. Duis sit amet consectetur neque, eu sodales odio. Donec sed elit nec ligula vehicula aliquet. Fusce ac nisi non elit facilisis viverra. Aenean interdum lobortis ultrices. Fusce scelerisque dignissim est eget efficitur.

          Sed vulputate non ante nec efficitur. Praesent sed sapien vel augue volutpat pharetra. Aliquam commodo nunc non lorem vehicula tincidunt. Nam sagittis arcu sit amet nulla vulputate posuere. Aliquam erat volutpat. Nulla nec ante urna. Nam neque erat, congue eget pulvinar sit amet, vulputate et dui. Nunc vulputate tempus lectus, eu lacinia orci bibendum eu. Suspendisse semper tellus non justo tempor, nec iaculis ligula sagittis. Proin vitae magna venenatis, posuere ligula ut, dignissim urna. Vestibulum efficitur semper accumsan. Aliquam ac velit eget arcu dapibus ornare.

          Pellentesque sodales diam libero, a malesuada massa ultricies in. Praesent eleifend volutpat lorem, quis bibendum ex fringilla ac. Integer non elit sed tellus ornare elementum sit amet quis elit. Nullam bibendum consequat nunc, at efficitur erat volutpat vitae. Integer in sodales ex. Mauris porta dui dolor. Duis non lacinia eros. Vestibulum sem lorem, ullamcorper ultricies consectetur in, semper in orci. Donec malesuada auctor ex, ut fermentum ante vestibulum vitae. Quisque porttitor nisi vel egestas varius. In bibendum elit nisi, ut molestie ex hendrerit sit amet.

          Sed id lorem at lorem sagittis cursus eget in purus. Phasellus posuere enim nisi, id ultricies eros varius ac. Ut eu lacus nec arcu eleifend consectetur sit amet vitae dolor. Praesent aliquam turpis nibh, vitae viverra mi dapibus eget. Fusce pulvinar dolor nibh, quis lacinia purus elementum venenatis. Nunc eu eros sed magna pulvinar rutrum. Ut vel malesuada risus. Fusce turpis ex, egestas vel pharetra cursus, convallis id lacus. Proin consectetur molestie mi, vitae efficitur mi consequat vel. Aliquam rutrum ac risus id ultrices. Donec aliquet venenatis sagittis. Suspendisse vitae euismod leo. Cras a fringilla turpis. Aliquam urna massa, lacinia ac justo vitae, dapibus imperdiet felis. Fusce laoreet malesuada consequat.
        `
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
  width: 95%;
}

.custom-scrollspy {
  position: relative;
  overflow-y: auto;
  height: 38vw;
}

.custom-content-card {
  width: 95%;
}

@media (max-width: 985px) {
  .my_component {
    width: 100%;
  }

  .custom-scrollspy {
    height: 100%;
  }

  .custom-content-card {
    width: 100%;
  }
}
</style>
