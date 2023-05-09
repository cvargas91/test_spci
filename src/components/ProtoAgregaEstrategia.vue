<template>
  <div class="q-gutter-md" style="min-width: 300px">
    <q-select
      filled
      v-model="estrategia"
      :options="estrategias"
      stack-label
      label="Seleccione una estrategia"
      color="primary"
    >
      <template v-slot:selected-item="scope">
        <q-item v-bind="scope.itemProps">
          <q-item-section>
            <q-item-label>{{ scope.opt.id_uaysen }}</q-item-label>
            <q-item-label caption>
              <q-badge v-if="scope.opt.ambito" color="black">{{
                scope.opt.ambito
              }}</q-badge>
              {{ scope.opt.descripcion }}
            </q-item-label>
          </q-item-section>
        </q-item>
      </template>
      <template v-slot:option="scope">
        <q-item v-bind="scope.itemProps">
          <q-item-section>
            <q-item-label>{{ scope.opt.id_uaysen }}</q-item-label>
            <q-item-label caption>
              <q-badge v-if="scope.opt.ambito" color="black">{{
                scope.opt.ambito
              }}</q-badge>
              {{ scope.opt.descripcion }}
            </q-item-label>
          </q-item-section>
        </q-item>
      </template>
    </q-select>
    <div class="q-gutter-xs">
      <q-btn
        label="Añadir"
        type="button"
        color="primary"
        class="q-mr-sm"
        @click="aniadirEstrategia"
        :disable="!estrategia"
      />
      <q-btn color="btnCancelar" label="Cancelar" @click="clicCancelar" />
    </div>
  </div>
</template>

<script>
import { computed, ref, onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";

export default {
  props: { mostrar: Boolean, id_accion: Number },
  setup(props, { emit }) {
    const estrategias = computed(() => store.state.estrategia.estrategias);
    const estrategia = ref(null);
    const store = useStore();
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    onMounted(() => {
      if (!estrategias.value.length)
        store.dispatch("estrategia/reqEstrategias");
    });
    onUnmounted(() => {
      estrategia.value = null;
    });
    return {
      estrategia,
      estrategias,
      aniadirEstrategia: () => {
        mostrar.value = false;
        store.dispatch("poador/agregaEstrategia", {
          id_accion: props.id_accion,
          id_estrategia: estrategia.value.id,
        });
      },
      clicCancelar: () => {
        mostrar.value = false;
      },
    };
  },
};
</script>
