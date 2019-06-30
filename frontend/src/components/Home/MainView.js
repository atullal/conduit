import ArticleList from '../ArticleList';
import React from 'react';
import { connect } from 'react-redux';

const mapStateToProps = state => ({
  articles: state.articles
});

const MainView = props => {
  return (
    <div className="col-md-9">
      <div className="feed-toggle">
        <ul className="nav outline-active">

        <li className="">
          <a
            href=""
            className="active">
            Global Feed
          </a>
        </li>

        </ul>
      </div>

      <ArticleList
        articles={props.articles} />
    </div>
  );
};

export default connect(mapStateToProps, () => ({}))(MainView);
