import React from 'react';

const ArticlePreview = props => {
  const article = props.article;

  return (
    <div className="article-preview">
    
    <div className="row row-eq-height">
    <div className="col-md-9 text-container">
      <a to={`article/${article.slug}`} className="preview-link">
        <h1>{article.title}</h1>
        <p>{article.description}</p>
      </a>
      <div className="article-meta">
        <a>
          <img src={article.author.image} />
        </a>

        <div className="info">
          <a className="author">
            {article.author.username}
          </a>
          <span className="date">
            {new Date(article.createdAt).toDateString()}
          </span>
        </div>

        {/* <div className="pull-xs-right">
            <i className="ion-heart"></i> {article.favoritesCount}
        </div> */}
      </div>
      </div>
      <div className="img-container col-md-2">
        <img className="article-image" src="https://data.whicdn.com/images/297177792/large.jpg"/>
        </div>
        </div>
    </div>
  );
}

export default ArticlePreview;
