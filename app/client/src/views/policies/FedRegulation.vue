<template>
  <h5>
    <b-badge
      :href="link"
      target="_blank"
      pill
      variant="light"
      class="p-2 m-2"
      style="border: 1px solid black;"
    >
      <!-- {{ regulation.title }} CFR {{ (regulation?.chapter ? regulation.chapter : '') + (regulation?.subchapter ? '.' + regulation.subchapter : '') }} {{ (regulation?.part ? '§' + regulation.part : '') + (regulation?.subpart ? '.' + regulation.subpart : '') }} {{ regulation?.section ? '§' + regulation.section : '' }} -->
      {{ regulation.title }} CFR {{ (regulation?.part ? '§' + regulation.part : '') + (regulation?.subpart ? '.' + regulation.subpart : '') }} {{ regulation?.section ? '§' + regulation.section : '' }}
    </b-badge>
  </h5>
</template>

<script>
export default {
  name: 'FedRegulation',
  props: {
    regulation: {
      type: Object,
      required: true
    }
  },
  data () {
    return {}
  },
  computed: {
    link: function () {
      let url = 'https://www.ecfr.gov/'

      // Handle Date
      if (this.regulation.regulation_date) {
        url += this.regulation.regulation_date + '/'
      } else {
        url += 'current/'
      }

      // Handle Title
      if (this.regulation.title) {
        url += 'title-' + this.regulation.title + '/'
      }

      if (this.regulation.section) {
        url += 'section-' + this.regulation.section + '/'
        return url
      }

      // // Handle Chapter
      // if (this.regulation.chapter) {
      //   url += 'chapter-' + this.regulation.chapter + '/'
      // }

      // // Handle Subchapter
      // if (this.regulation.subchapter) {
      //   url += 'subchapter-' + this.regulation.subchapter + '/'
      // }

      // // Handle Part
      // if (this.regulation.part) {
      //   url += 'part-' + this.regulation.part + '/'
      // }

      // // Handle Subpart
      // if (this.regulation.subpart) {
      //   url += '#' + this.regulation.part + '.' + this.regulation.subpart
      // }

      // Handle Part
      if (this.regulation.part) {
        url += 'section-' + this.regulation.part
      }

      // Handle Subpart
      if (this.regulation.subpart) {
        url += '.' + this.regulation.subpart
      }

      return url
    }
  }
}
</script>
