<template>
  <q-page>
    <div class="q-pa-md">
      <div class="" v-if="accion.estrategias">
        <ApexHeatmap :datos="accion.estrategias" />
      </div>
      <div v-else>Cargando... Gracias por esperar</div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, onMounted, onUnmounted, ref, computed } from "vue";
import { useStore, mapState } from "vuex";
import ApexHeatmap from "src/components/ApexHeatmap.vue";

export default defineComponent({
  components: {
    ApexHeatmap,
  },
  setup() {
    const store = useStore();
    onMounted(() => {
      store.dispatch("accion/reqEstrategias");
    });
    return {};
  },
  computed: {
    ...mapState(["accion", "usuarix"]),
  },
});
</script>
