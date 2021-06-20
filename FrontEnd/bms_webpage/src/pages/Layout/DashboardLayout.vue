<template>
  <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
    <side-bar
      v-if="this.$route.path == '/login' ? false : true"
      :sidebar-item-color="sidebarBackground"
      :sidebar-background-image="sidebarBackgroundImage"
    >
      <mobile-menu slot="content"></mobile-menu>

      <sidebar-link to="/dashboard" v-if="this.role==0 ? true : false">
        <md-icon>dashboard</md-icon>
        <p>总览</p>
      </sidebar-link>
      <sidebar-link to="/user">
        <md-icon>person</md-icon>
        <p v-if="this.role==0 ? true : false">用户管理</p>
        <p v-if="this.role!=0 ? true : false">修改密码</p>
      </sidebar-link>
      <sidebar-link to="/importtable" v-if="this.role==0||this.role==2 ? true : false">
        <md-icon>content_paste</md-icon>
        <p>进货管理</p>
      </sidebar-link>
      <sidebar-link
        to="/storetable"
        v-if="this.role==0||this.role==1||this.role==4  ? true : false"
      >
        <md-icon>store</md-icon>
        <p v-if="this.role==0||this.role==1  ? true : false">库存管理</p>
        <p v-if="this.role==4  ? true : false">入库</p>
      </sidebar-link>
      <sidebar-link to="/saletable" v-if="this.role==0||this.role==3||this.role==5  ? true : false">
        <md-icon>bubble_chart</md-icon>
        <p v-if="this.role==0||this.role==3  ? true : false">销售管理</p>
        <p v-if="this.role==5  ? true : false">销售</p>
      </sidebar-link>
      <!--
      <sidebar-link to="/maps">
        <md-icon>location_on</md-icon>
        <p>Maps</p>
      </sidebar-link>-->
      <!--
      <sidebar-link to="/notifications">
        <md-icon>notifications</md-icon>
        <p>Notifications</p>
      </sidebar-link>
      
      <sidebar-link to="/upgrade" class="active-pro">
        <md-icon>unarchive</md-icon>
        <p>Upgrade to PRO</p>
      </sidebar-link>-->
    </side-bar>

    <div class="main-panel" v-if="this.$route.path == '/login' ? false : true">
      <top-navbar></top-navbar>

      <fixed-plugin :color.sync="sidebarBackground" :image.sync="sidebarBackgroundImage"></fixed-plugin>

      <dashboard-content></dashboard-content>

      <content-footer v-if="!$route.meta.hideFooter"></content-footer>
    </div>
    <dashboard-content v-if="this.$route.path != '/login' ? false : true"></dashboard-content>
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "@/pages/Layout/MobileMenu.vue";
//import FixedPlugin from "./Extra/FixedPlugin.vue";
import Cookies from "js-cookie";

export default {
  components: {
    TopNavbar,
    DashboardContent,
    ContentFooter,
    MobileMenu
  },
  data() {
    return {
      sidebarBackground: "purple",
      sidebarBackgroundImage: require("@/assets/img/sidebar-black.jpg"),
      showdashboard: true,
      role: Cookies.get("role")
    };
  },
};
</script>
