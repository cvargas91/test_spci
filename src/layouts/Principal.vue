<style scoped>
#logo {
  width: 10em;
  height: auto;
  padding: 0.2em;
}
</style>
<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="fondoSuperior">
      <q-toolbar>
        <q-btn
          color="textoAzul"
          dense
          flat
          round
          icon="menu"
          @click="toggleLeftDrawer"
        />
        <q-toolbar-title>
          <q-btn size="lg" flat to="/" padding="none">
            <img
              id="logo"
              src="/static/Colabora-logo_recortado.png"
              width="1px"
              height="10px"
            />
          </q-btn>
        </q-toolbar-title>
        <span class="text-textoAzul">
          {{ timeSession() }}<b>{{ usuario.nombre }} {{ usuario.apellido }}</b
          >,
          {{ usuario.perfil.esEncargado ? "Encargado de " : "" }}
          {{ usuario.perfil.actor_nombre }}</span
        >
        <q-avatar>
          <img :src="usuario.perfil.foto" />
        </q-avatar>
        <q-btn
          v-if="usuario.perfil.esMultiPerfil"
          icon="switch_account"
          dense
          flat
          round
          @click="cambiaPerfil"
          color="positive"
        ></q-btn>
        <q-btn
          icon="logout"
          dense
          flat
          round
          @click="logout"
          color="positive"
        ></q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer
      show-if-above
      v-model="leftDrawerOpen"
      side="left"
      class="fondoIzquierda"
    >
      <q-list>
        <q-item-label header></q-item-label>
        <MenuIzquierda
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { useQuasar } from "quasar";
import { ref, computed } from "vue";
import { useStore } from "vuex";
import MenuIzquierda from "src/components/MenuIzquierda.vue";

export default {
  components: {
    MenuIzquierda,
  },
  methods: {
    timeSession() {
      let second = 0;
      let interval = setInterval(() => {
        if (second === 3600) {
          clearInterval(interval);
          this.logout();
        } else {
          second++;
        }
      }, 1000);
    },
  },
  setup() {
    const store = useStore();
    const usuario = computed(() => store.state.usuarix.usuario);
    const leftDrawerOpen = ref(false);
    const rightDrawerOpen = ref(false);

    const $q = useQuasar();
    const linksList = ref([
      {
        title: "Acciones Institucionales",
        caption:
          "Listado de compromisos institucionales en acciones del Plan de Mejora Institucional, Proyectos Institucionales y Prioridades Transversales",
        icon: "groups",
        link: "acciones",
      },

      /*Se inhabilita boton hasta validar nuevo uso */
      /*{

        title: "Acciones PMI",
        caption: "Lista y detalle de las acciones del plan de mejora",
        icon: "insights",
        link: "accionesPMI",
      },*/
      {
        title: "Bandeja de entregas",
        caption: "Estado de entregas de productos y verificadores",
        icon: "inbox",
        link: "bandejaEntregas",
      },
      {
        title: "Navegador POA",
        caption: "Acciones del Plan de Mejora Institucional de la Universidad",
        icon: "sailing",
        link: "navegadorPOA",
      },
      {
        title: "Retroalimentaciones",
        caption: "Retroalimentación de productos y verificadores rechazados",
        icon: "feedback",
        link: "retroalimentaciones",
      },
      /* Se trabaja en sección de ayuda para ayudar a los posibles problemas o dudas de usuarios*/
      /*{
        title: "Ayuda",
        caption: "Resolución de dudas y consultas",
        icon: "help",
        link: "ayuda",
      },*/
    ]);

    $q.dark.set(false);

    if (usuario.value.perfil.esAnalistaUPCI) {
      linksList.value.splice(
        1,
        0,
        {
          title: "Bandeja UPCI",
          caption: "Estado de entregas para ser revisadas por equipo UPCI",
          icon: "checklist_rtl",
          link: "bandejaUPCI",
        },
        {
          title: "Reportes",
          caption: "Generación de reportes por unidades y acciones",
          icon: "feed",
          link: "panelReportesUpci",
        },
        /*Se inhabilita botón de creador, de momento se utilizará funcionalidad desde Admin*
        /*{
          title: "Creador POAs",
          caption: "Diseño de nuevas acciones para un nuevo periodo",
          icon: "add_circle",
          link: "creadorPOAs",
        }*/
      );
    }

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleDarkMode() {
        $q.dark.toggle();
      },
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
      rightDrawerOpen,
      toggleRightDrawer() {
        rightDrawerOpen.value = !rightDrawerOpen.value;
      },
      logout() {
        window.location.href = "/logout";
      },
      cambiaPerfil() {
        window.location.href = "/";
      },
      usuario,
    };
  },
};
</script>
