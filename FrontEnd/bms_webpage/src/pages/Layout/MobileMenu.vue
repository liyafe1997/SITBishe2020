<template>
  <ul class="nav nav-mobile-menu">
    <!--
    <li>
      <md-field>
        <label>Search</label>
        <md-input v-model="search" type="text"></md-input>
      </md-field>
    </li>
    <li>
      <a href="#" class="dropdown-toggle" data-toggle="dropdown">
        <i class="material-icons">dashboard</i>
        <p>Dashboard</p></a
      >
    </li>
    <li>
      <drop-down>
        <a slot="title" class="dropdown-toggle" data-toggle="dropdown">
          <i class="material-icons">notifications</i>
          <span class="notification">5</span>
          <p>Notifications</p>
        </a>
        <ul class="dropdown-menu dropdown-menu-right">
          <li><a href="#">Mike John responded to your email</a></li>
          <li><a href="#">You have 5 new tasks</a></li>
          <li><a href="#">You're now friend with Andrew</a></li>
          <li><a href="#">Another Notification</a></li>
          <li><a href="#">Another One</a></li>
        </ul>
      </drop-down>
    </li>
    <li>
      <a href="#" data-toggle="dropdown" class="dropdown-toggle"
        ><i class="material-icons">person</i>
        <p>Profile</p></a
      >
    </li>
    -->
    <li>
      <drop-down>
        <a slot="title" class="dropdown-toggle" data-toggle="dropdown">
          <p>{{this.username}}&nbsp;{{this.roletext}}</p>
        </a>
        <ul class="dropdown-menu dropdown-menu-right">
          <li>
            <a v-on:click="logout" href="javascript:void(0);">退出登录</a>
          </li>
        </ul>
      </drop-down>
    </li>
  </ul>
</template>
<script>
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  data() {
    return {
      roletext: "",
      username: ""
    };
  },
  mounted() {
    let role = Cookies.get("role");
    if (role == 0) {
      this.roletext = "系统管理员";
    } else if (role == 1) {
      this.roletext = "库存管理员";
    } else if (role == 2) {
      this.roletext = "进货管理员";
    } else if (role == 3) {
      this.roletext = "销售管理员";
    } else if (role == 4) {
      this.roletext = "入库员";
    } else if (role == 5) {
      this.roletext = "销售员";
    }
    this.username = Cookies.get("username");
  },

  methods: {
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    logout() {
      Cookies.remove("username");
      Cookies.remove("token");
      Cookies.remove("role");
      this.$router.replace("/login");
    }
  }
};
</script>

