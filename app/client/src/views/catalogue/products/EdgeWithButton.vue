<template>
  <EdgeLabelRenderer>
    <div
      :style="{
        pointerEvents: 'all',
        position: 'absolute',
        transform: `translate(-50%, -50%) translate(${path[1]}px,${path[2]}px)`,
        backgroundColor: 'white'
      }"
      class="nodrag nopan"
    >
      <b-button variant="outline-danger" v-show="edit" class="edgebutton" @click="deleteEdge()"><b-icon icon="trash"></b-icon></b-button>
    </div>
  </EdgeLabelRenderer>
</template>

<script>
import { EdgeLabelRenderer, getSmoothStepPath } from '@vue-flow/core'

export default {
  components: {
    EdgeLabelRenderer
  },
  inheritAttrs: false,
  props: {
    id: {
      type: String,
      required: true
    },
    edit: {
      type: Boolean,
      required: true
    },
    sourceX: {
      type: Number,
      required: true
    },
    sourceY: {
      type: Number,
      required: true
    },
    targetX: {
      type: Number,
      required: true
    },
    targetY: {
      type: Number,
      required: true
    },
    sourcePosition: {
      type: String,
      required: true
    },
    targetPosition: {
      type: String,
      required: true
    },
    markerEnd: {
      type: String,
      required: false
    },
    customStyle: {
      type: Object,
      required: false
    }
  },
  methods: {
    deleteEdge () {
      this.$emit('deleteEdge', this.id)
    }
  },
  computed: {
    path: function () {
      const props = {
        id: this.id,
        sourceX: this.sourceX,
        sourceY: this.sourceY,
        targetX: this.targetX,
        targetY: this.targetY,
        sourcePosition: this.sourcePosition,
        targetPosition: this.targetPosition,
        markerEnd: this.markerEnd,
        customStyle: this.customStyle
      }
      return getSmoothStepPath(props)
    }
  }
}
</script>
