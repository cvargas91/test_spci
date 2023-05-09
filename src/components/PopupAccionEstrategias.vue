<template>
  <q-dialog v-model="mostrar">
    <q-card class="col-xxl-5" style="width: 250%">
      <q-card-section class="text-textoAzul">
        <q-card-section align="right" class="text-weight-medium">
          <b>Estrategias</b>
        </q-card-section>
        <q-separator color="indigo-10" />
        <div>Acción Seleccionada:</div>
        <div class="text-h6 text-textoAzul">
          <b>{{accion.accion.id_uaysen}}. {{ accion.accion.titulo }}</b>
        </div>
        <div v-if="estrategias.length">
          <q-list bordered separator padding>
            <q-item v-for="item in estrategias" :key="item.id">
              <q-item-section>
                <q-item-label overline class="text-textoAzul"><b>Estrategia: {{ item.id_uaysen }}</b></q-item-label>
                <q-item-label>{{ item.descripcion }}</q-item-label>
                <q-item-label caption>
                  {{ item.ambito }}
                </q-item-label>
              </q-item-section>
              <q-item-section side top>
                <q-item-label caption
                  >{{ item.periodo.anio_inicio }}-{{
                    item.periodo.anio_fin
                  }}</q-item-label
                >
              </q-item-section>
            </q-item>
          </q-list>
        </div>
        <div v-else>
          <q-banner class="bg-primary">
            No hay estrategias asociadas a la acción seleccionada. Agradeceremos
            notificar a UPCI
          </q-banner>
        </div>
      </q-card-section>
      <q-card-actions align="center">
        <q-btn label="ACEPTAR" color="secondary" text-color="white" v-close-popup class="Full-width"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { computed } from "vue";

export default {
  props: {
    mostrar: Boolean,
    estrategias: Array,
    accion: Object,
  },
  setup(props, { emit }) {
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    const estrategias = props.estrategias;
    const accion = props.accion;
    return {
      mostrar,
      estrategias,
      accion,
    };
  },
};
</script>
