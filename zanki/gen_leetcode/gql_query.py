questionSolutionArticlesQuery = """
query questionSolutionArticles($questionSlug: String!, $skip: Int, $first: Int, $orderBy: SolutionArticleOrderBy, $userInput: String) {
  questionSolutionArticles(questionSlug: $questionSlug, skip: $skip, first: $first, orderBy: $orderBy, userInput: $userInput) {
    totalNum
    edges {
      node {
        ...article
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment article on SolutionArticleNode {
  title
  slug
  reactedType
  status
  identifier
  canEdit
  reactions {
    count
    reactionType
    __typename
  }
  tags {
    name
    nameTranslated
    slug
    __typename
  }
  createdAt
  thumbnail
  author {
    username
    profile {
      userAvatar
      userSlug
      realName
      __typename
    }
    __typename
  }
  summary
  topic {
    id
    commentCount
    viewCount
    __typename
  }
  byLeetcode
  isMyFavorite
  isMostPopular
  isEditorsPick
  upvoteCount
  upvoted
  hitCount
  __typename
}
"""

getQuestionDetailQuery = """
query getQuestionDetail($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        questionTitle
        questionTitleSlug
        content
        translatedTitle
        translatedContent
        difficulty
        stats
        similarQuestions
        categoryTitle
        topicTags {
            name
            slug
        }
    }
}
"""

solutionDetailArticleQuery = """
query solutionDetailArticle($slug: String!) {
  solutionArticle(slug: $slug) {
    ...article
    content
    __typename
  }
}

fragment article on SolutionArticleNode {
  title
  slug
  reactedType
  status
  identifier
  canEdit
  reactions {
    count
    reactionType
    __typename
  }
  tags {
    name
    nameTranslated
    slug
    __typename
  }
  createdAt
  thumbnail
  author {
    username
    profile {
      userAvatar
      userSlug
      realName
      __typename
    }
    __typename
  }
  summary
  topic {
    id
    commentCount
    viewCount
    __typename
  }
  byLeetcode
  isMyFavorite
  isMostPopular
  isEditorsPick
  upvoteCount
  upvoted
  hitCount
  __typename
}
"""
