import { Fragment } from "react";

import Navbar from "./Navbar";

import classes from "./layout.module.css";

// For basic layout of every app page
function Layout(props) {
  // Must always include navbar attached to the children around which the <Layout> component will be wrapped
  return (
    <Fragment>
      <Navbar />
      <main className={classes.main}>{props.children}</main>
    </Fragment>
  );
}

export default Layout;
