<template>
  <q-card class="my-card" v-if="usuario.perfil">
    <q-item>
      <q-item-section avatar>
        <q-avatar>
          <img :src="usuario.perfil.foto" />
        </q-avatar>
      </q-item-section>

      <q-item-section>
        <q-item-label>{{ usuario.nombre }} {{ usuario.apellido }}</q-item-label>
        <q-item-label caption>
          {{ usuario.perfil.esEncargado ? "Encargado de " : "" }}
          {{ usuario.perfil.actor_nombre }}
        </q-item-label>
      </q-item-section>
    </q-item>
  </q-card>
</template>

<script>
import { computed, defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  name: "MenuDerecha",
  setup() {
    const store = useStore();
    return {
      usuario: computed(() => store.state.usuarix.usuario),
    };
  },
});
</script>
