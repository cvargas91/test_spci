<template>
  <q-dialog v-model="mostrar">
    <q-card style="width: 700px; max-width: 80vw">
      <q-card-section>
        <div class="text-h6">Nueva propuesta de Acción</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        Ingrese un título, objetivo y tipo para la nueva Acción<br />(Podrá
        hacer modificaciones más tarde)
      </q-card-section>
      <q-card-section>
        <div class="q-gutter-md">
          <q-input
            standout
            bottom-slots
            v-model="id_uaysen"
            label="Código Interno"
            readonly
          >
            <template v-slot:hint>
              El identificador de acción se generará al momento de su creación
            </template>
          </q-input>
          <q-input v-model="titulo" label="Título" />
          <q-input v-model="objetivo" label="Objetivo" type="textarea" />
          <q-select v-model="tipo" :options="tiposAccion" label="Tipo" />
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Cancelar" color="btnCancelar" v-close-popup />
        <q-btn
          flat
          label="Añadir"
          :disable="!titulo || !objetivo || !tipo"
          color="primary"
          @click="clicAniadir"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";

export default {
  props: {
    mostrar: Boolean,
  },
  setup(props, { emit }) {
    const idUsuario = computed(() => store.state.usuarix.usuario.id);
    const prefijoArea = computed(
      () => store.state.usuarix.usuario.perfil.area_sigla
    );
    const idUnidad = computed(
      () => store.state.usuarix.usuario.perfil.actor_id
    );
    const titulo = ref("");
    const objetivo = ref("");
    const tipo = ref("");
    const store = useStore();
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    return {
      mostrar,
      id_uaysen: ref(prefijoArea.value + "-..."),
      titulo,
      objetivo,
      tipo,
      tiposAccion: ["Misional", "Desarrollo"],
      clicAniadir: () => {
        store.dispatch("poador/reqNuevaAccion", {
          creador: idUsuario.value,
          unidad: idUnidad.value,
          titulo: titulo.value,
          objetivo: objetivo.value,
          tipo: tipo.value,
        });
        mostrar.value = false;
      },
      idUnidad,
    };
  },
};
</script>
