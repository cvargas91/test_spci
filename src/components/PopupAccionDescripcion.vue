<template>
  <q-dialog v-model="mostrar">
    <q-card class="col-xxl-5" style="width: 250%">
      
      <q-card-section class="text-textoAzul" >
        <q-card-section align="right" class="text-weight-medium">
          <b>Descripción</b>
        </q-card-section>
        <q-separator color="indigo-10" />

        <div>Acción Seleccionada:</div>
        <div class="text-h6 text-textoAzul">
          <b>{{accion.accion.id_uaysen}}. {{ accion.accion.titulo }}</b>
        </div>
        <p><b>Objetivo:</b> {{ accion.accion.objetivo }}</p>
        <p>
          <b>{{ accion.tipo }}</b> : {{ accion.actor.nombre }} ({{
            accion.actor.sigla
          }})
          <span v-if="accion.actor.dependencia">
            , {{ accion.actor.dependencia.nombre }} ({{
              accion.actor.dependencia.sigla
            }})
          </span>
        </p>
      </q-card-section>
      <q-card-actions align="center">
        <q-btn label="ACEPTAR" color="secondary" text-color="white" v-close-popup class="Full-width"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default {
  props: {
    mostrar: Boolean,
    accion: Object,
  },
  setup(props, { emit }) {
    const store = useStore();
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    const accion = props.accion;
    return {
      mostrar,
      accion,
    };
  },
};
</script>
