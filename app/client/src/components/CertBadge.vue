<template>
  <span v-if="data != null">
    <span v-for="cert, index in certs" :key="index">
      <span v-if="cert.key && data[cert.key]">
        <b-img :id="'cert' + index + cert.r" style="width:4em;" circle class="mr-2 p-2" :src="cert.img"></b-img>
        <b-tooltip :target="'cert' + index + cert.r" triggers="hover">{{ cert.alt }}</b-tooltip>
      </span>
    </span>
  </span>
</template>

<script>
export default {
  name: 'CertBadge',
  props: ['data'],
  data: function () {
    return {
      certs: [
        {
          key: 'certified_usda_organic',
          img: require('../assets/certifications/usda_organic.png'),
          alt: 'Certified USDA Organic',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_wildcrafted',
          img: require('../assets/certifications/wildcrafted.png'),
          alt: 'Certified Wild Crafted',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_made_with_organic',
          img: require('../assets/certifications/made_with_organic.png'),
          alt: '70% Organic',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_fda',
          img: require('../assets/certifications/fda_approved.png'),
          alt: 'FDA Approved',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_gluten_free',
          img: require('../assets/certifications/gluten_free.png'),
          alt: 'Certified Gluten Free',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_gmp',
          img: require('../assets/certifications/good_manufacturing_practice.png'),
          alt: 'Certified Good Manufacturing Practice',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_halal',
          img: require('../assets/certifications/halal_certified.png'),
          alt: 'Certified Halal',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_kosher',
          img: require('../assets/certifications/kosher_certified.png'),
          alt: 'Certified Kosher',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_national_sanitation_foundation',
          img: require('../assets/certifications/nsf_international_logo.png'),
          alt: 'National Sanitation Foundation',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_us_pharmacopeia',
          img: require('../assets/certifications/us_pharmacopeia.png'),
          alt: 'US Pharmacopeia',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_vegan',
          img: require('../assets/certifications/vegan.png'),
          alt: 'Certified Vegan',
          r: Math.floor(Math.random() * 1000)
        },
        {
          key: 'certified_non_gmo',
          img: require('../assets/certifications/non_gmo.png'),
          alt: 'Non-GMO',
          r: Math.floor(Math.random() * 1000)
        }
      ]
    }
  }
}
</script>
