import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import Dashboard from "@/pages/Dashboard.vue";
import Login from "@/pages/Login.vue";

import UserTableList from "@/pages/UserTableList.vue";
import ImportTableList from "@/pages/ImportTableList.vue";
import SaleTableList from "@/pages/SaleTableList.vue";
import StoreTableList from "@/pages/StoreTableList.vue";
const routes = [
  {
    path: "/",
    component: DashboardLayout,
    redirect: "/login",
    children: [
      {
        path: "login",
        name: "用户登录",
        component: Login
      },
      {
        path: "dashboard",
        name: "总览",
        component: Dashboard
      },
      {
        path: "user",
        name: "用户管理",
        component: UserTableList
      },
      {
        path: "importtable",
        name: "进货管理",
        component: ImportTableList
      },
      {
        path: "saletable",
        name: "销售管理",
        component: SaleTableList
      },
      {
        path: "storetable",
        name: "库存管理",
        component: StoreTableList
      }
    ]
  }
];

export default routes;
