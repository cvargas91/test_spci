const routes = [
  {
    path: "/",
    component: () => import("src/layouts/Principal.vue"),
    children: [
      { path: "", component: () => import("pages/Index.vue") },
      {
        path: "bandejaEntregas",
        component: () => import("pages/BandejaEntregas.vue"),
      },
      {
        path: "bandejaUPCI",
        component: () => import("pages/BandejaUPCI.vue"),
      },
      {
        path: "acciones",
        component: () => import("src/pages/Acciones.vue"),
      },
      {
        path: "accionesPMI",
        component: () => import("src/pages/AccionesPMI.vue"),
      },
      { path: "navegadorPOA", component: () => import("pages/Navegador.vue") },
      {
        path: "subirProducto",
        component: () => import("src/pages/SubirProducto.vue"),
      },
      {
        path: "subirVerificador",
        component: () => import("src/pages/SubirVerificador.vue"),
      },
      { path: "matrizPOA", component: () => import("pages/Matriz.vue") },
      {
        path: "rechazaEntrega",
        component: () => import("pages/RechazaEntrega.vue"),
      },
      {
        path: "retroalimentaciones",
        component: () => import("pages/Retroalimentaciones.vue"),
      },
      {
        path: "editaVerificador",
        component: () => import("pages/EditaVerificador.vue"),
      },
      {
        path: "editaProducto",
        component: () => import("pages/EditaProducto.vue"),
      },
      {
        path: "panelReportesUpci",
        component: () => import("pages/PanelReportesUpci.vue"),
      },
      {
        path: "finalizaEntregaUPCI",
        component: () => import("pages/FinalizaEntregaUPCI.vue"),
      },
      {
        path: "reporteUpci",
        component: () => import("src/pages/ReporteUpci.vue"),
      },
      {
        path: "reporteUpciEdicion",
        component: () => import("src/pages/ReporteUpciEdicion.vue"),
      },
      {
        path: "reporteUpciPMI",
        component: () => import("src/pages/ReporteUpciPMI.vue"),
      },      
      {
        path: "reporteUpciEdicionPMI",
        component: () => import("src/pages/ReporteUpciEdicionPMI.vue"),
      },
      {
        path: "creadorPOAs",
        component: () => import("pages/CreadorPOAs.vue"),
      },
      {
        path: "bandejaUnidades",
        component: () => import("src/components/BandejaUnidades.vue"),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
