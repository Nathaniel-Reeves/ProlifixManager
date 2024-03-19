<template>
  <span>
    <span v-for="cert, index in certs" :key="index">
      <span v-if="cert.key && data[cert.key]">
        <b-img :id="'cert' + index" style="width:2em;" circle class="ml-2" :src="cert.img"></b-img>
        <b-tooltip :target="'cert' + index" triggers="hover">{{ cert.alt }}</b-tooltip>
      </span>
    </span>
  </span>
</template>

<script>
export default {
  name: 'CertBadge',
  props: {
    data: Object
  },
  data: function () {
    return {
      certs: [
        {
          key: '',
          img: require('../assets/certifications/fda_approved.png'),
          alt: 'FDA Approved'
        },
        {
          key: 'certified_gluten_free',
          img: require('../assets/certifications/gluten_free.png'),
          alt: 'Certified Gluten Free'
        },
        {
          key: '',
          img: require('../assets/certifications/good_manufacturing_practice.png'),
          alt: 'Certified Good Manufacturing Practice'
        },
        {
          key: 'certified_halal',
          img: require('../assets/certifications/halal_certified.png'),
          alt: 'Certified Halal'
        },
        {
          key: 'certified_kosher',
          img: require('../assets/certifications/kosher_certified.png'),
          alt: 'Certified Kosher'
        },
        {
          key: 'certified_national_sanitation_foundation',
          img: require('../assets/certifications/nsf_international_logo.png'),
          alt: 'National Sanitation Foundation'
        },
        {
          key: 'certified_us_pharmacopeia',
          img: require('../assets/certifications/us_pharmacopeia.png'),
          alt: 'US Pharmacopeia'
        },
        {
          key: 'certified_usda_organic',
          img: require('../assets/certifications/usda_organic.png'),
          alt: 'Certified USDA Organic'
        },
        {
          key: '',
          img: require('../assets/certifications/wildcrafted.png'),
          alt: 'Certified Wild Crafted'
        },
        {
          key: '',
          img: require('../assets/certifications/made_with_organic.png'),
          alt: '70% Organic'
        },
        {
          key: 'certified_vegan',
          img: require('../assets/certifications/vegan.png'),
          alt: 'Certified Vegan'
        }
      ]
    }
  }
}
</script>
