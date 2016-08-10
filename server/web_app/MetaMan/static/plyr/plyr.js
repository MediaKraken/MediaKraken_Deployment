



<!DOCTYPE html>
<html lang="en" class=" is-copy-enabled">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>

    <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/frameworks-536bcdee57776d99649d118d29a291c9d7b41d101696162d6456c87b07314253.css" integrity="sha256-U2vN7ld3bZlknRGNKaKRyde0HRAWlhYtZFbIewcxQlM=" media="all" rel="stylesheet" />
    <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/github-5db5a735a61ce0173ba56e5c51dec3a47371404e57c12965553f85500d781500.css" integrity="sha256-XbWnNaYc4Bc7pW5cUd7DpHNxQE5XwSllVT+FUA14FQA=" media="all" rel="stylesheet" />
    
    
    
    

    <link as="script" href="https://assets-cdn.github.com/assets/frameworks-e76ce42ce77c934586f7cacbe24d556dbe6fefdbe8b53a393644b18199f7c291.js" rel="preload" />
    
    <link as="script" href="https://assets-cdn.github.com/assets/github-427a64dc2d5702ced29c013da6c5c360faabebb96e58e6d427421d4466956150.js" rel="preload" />

    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">
    <meta name="viewport" content="width=device-width">
    
    
    <title>plyr/plyr.js at master · Meta-Man/plyr</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="/apple-touch-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="/apple-touch-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">
    <meta property="fb:app_id" content="1401488693436528">

      <meta content="https://avatars0.githubusercontent.com/u/12532343?v=3&amp;s=400" name="twitter:image:src" /><meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="Meta-Man/plyr" name="twitter:title" /><meta content="plyr - A simple HTML5, YouTube and Vimeo player" name="twitter:description" />
      <meta content="https://avatars0.githubusercontent.com/u/12532343?v=3&amp;s=400" property="og:image" /><meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="Meta-Man/plyr" property="og:title" /><meta content="https://github.com/Meta-Man/plyr" property="og:url" /><meta content="plyr - A simple HTML5, YouTube and Vimeo player" property="og:description" />
      <meta name="browser-stats-url" content="https://api.github.com/_private/browser/stats">
    <meta name="browser-errors-url" content="https://api.github.com/_private/browser/errors">
    <link rel="assets" href="https://assets-cdn.github.com/">
    <link rel="web-socket" href="wss://live.github.com/_sockets/ODgxNDQwNjowMTVhNGE0Y2U0OGZiOGE1YTUzZDk5NTcxNThhNDUwNjpjZTk2NmE3YWNhMWI4YzViZWU3ODE1NGQzY2U5ZTkwYTU5MWU2MWU3NmNlM2RmMzJmM2FlNGZhNDA1YzkwYWFi--c35e843df6eba13012881c42e734901213432823">
    <meta name="pjax-timeout" content="1000">
    <link rel="sudo-modal" href="/sessions/sudo_modal">

    <meta name="msapplication-TileImage" content="/windows-tile.png">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="selected-link" value="repo_source" data-pjax-transient>

    <meta name="google-site-verification" content="KT5gs8h0wvaagLKAVWq8bbeNwnZZK1r1XQysX3xurLU">
<meta name="google-site-verification" content="ZzhVyEFwb7w3e0-uOTltm8Jsck2F5StVihD0exw2fsA">
    <meta name="google-analytics" content="UA-3769691-2">

<meta content="collector.githubapp.com" name="octolytics-host" /><meta content="github" name="octolytics-app-id" /><meta content="D06B035A:3A83:123C71CB:5744B803" name="octolytics-dimension-request_id" /><meta content="8814406" name="octolytics-actor-id" /><meta content="SpootDev" name="octolytics-actor-login" /><meta content="946df5443abcdb370ccb0199bab49df2b539c5998aa16b2555e656a3185da2cb" name="octolytics-actor-hash" />
<meta content="/&lt;user-name&gt;/&lt;repo-name&gt;/blob/show" data-pjax-transient="true" name="analytics-location" />



  <meta class="js-ga-set" name="dimension1" content="Logged In">



        <meta name="hostname" content="github.com">
    <meta name="user-login" content="SpootDev">

        <meta name="expected-hostname" content="github.com">
      <meta name="js-proxy-site-detection-payload" content="OGE5NTliMDg3OGE0MWVjM2Y5YTI0ZGUxNjI3NTk1ZDZmYjRjMGY1ZDJkYzM4MzBmY2U3NTdiZTYxZTExMjJlMnx7InJlbW90ZV9hZGRyZXNzIjoiMjA4LjEwNy4zLjkwIiwicmVxdWVzdF9pZCI6IkQwNkIwMzVBOjNBODM6MTIzQzcxQ0I6NTc0NEI4MDMiLCJ0aW1lc3RhbXAiOjE0NjQxMjEzNTN9">


      <link rel="mask-icon" href="https://assets-cdn.github.com/pinned-octocat.svg" color="#4078c0">
      <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico">

    <meta name="html-safe-nonce" content="bad2ef507e6f482025edee8fd78f32eed4006f07">
    <meta content="f39c2a21a02fc39998e19fa7e5c58cfe76ce9a4b" name="form-nonce" />

    <meta http-equiv="x-pjax-version" content="0eeb39890ada13d0e4df1cb4118b9955">
    

      
  <meta name="description" content="plyr - A simple HTML5, YouTube and Vimeo player">
  <meta name="go-import" content="github.com/Meta-Man/plyr git https://github.com/Meta-Man/plyr.git">

  <meta content="12532343" name="octolytics-dimension-user_id" /><meta content="Meta-Man" name="octolytics-dimension-user_login" /><meta content="59605832" name="octolytics-dimension-repository_id" /><meta content="Meta-Man/plyr" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="true" name="octolytics-dimension-repository_is_fork" /><meta content="30794868" name="octolytics-dimension-repository_parent_id" /><meta content="Selz/plyr" name="octolytics-dimension-repository_parent_nwo" /><meta content="30794868" name="octolytics-dimension-repository_network_root_id" /><meta content="Selz/plyr" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/Meta-Man/plyr/commits/master.atom" rel="alternate" title="Recent Commits to plyr:master" type="application/atom+xml">


      <link rel="canonical" href="https://github.com/Meta-Man/plyr/blob/master/dist/plyr.js" data-pjax-transient>
  </head>


  <body class="logged-in   env-production linux vis-public fork page-blob">
    <div id="js-pjax-loader-bar" class="pjax-loader-bar"></div>
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>

    
    
    



        <div class="header header-logged-in true" role="banner">
  <div class="container clearfix">

    <a class="header-logo-invertocat" href="https://github.com/" data-hotkey="g d" aria-label="Homepage" data-ga-click="Header, go to dashboard, icon:logo">
  <svg aria-hidden="true" class="octicon octicon-mark-github" height="28" version="1.1" viewBox="0 0 16 16" width="28"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59 0.4 0.07 0.55-0.17 0.55-0.38 0-0.19-0.01-0.82-0.01-1.49-2.01 0.37-2.53-0.49-2.69-0.94-0.09-0.23-0.48-0.94-0.82-1.13-0.28-0.15-0.68-0.52-0.01-0.53 0.63-0.01 1.08 0.58 1.23 0.82 0.72 1.21 1.87 0.87 2.33 0.66 0.07-0.52 0.28-0.87 0.51-1.07-1.78-0.2-3.64-0.89-3.64-3.95 0-0.87 0.31-1.59 0.82-2.15-0.08-0.2-0.36-1.02 0.08-2.12 0 0 0.67-0.21 2.2 0.82 0.64-0.18 1.32-0.27 2-0.27 0.68 0 1.36 0.09 2 0.27 1.53-1.04 2.2-0.82 2.2-0.82 0.44 1.1 0.16 1.92 0.08 2.12 0.51 0.56 0.82 1.27 0.82 2.15 0 3.07-1.87 3.75-3.65 3.95 0.29 0.25 0.54 0.73 0.54 1.48 0 1.07-0.01 1.93-0.01 2.2 0 0.21 0.15 0.46 0.55 0.38C13.71 14.53 16 11.53 16 8 16 3.58 12.42 0 8 0z"></path></svg>
</a>


        <div class="header-search scoped-search site-scoped-search js-site-search" role="search">
  <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/Meta-Man/plyr/search" class="js-site-search-form" data-scoped-search-url="/Meta-Man/plyr/search" data-unscoped-search-url="/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
    <label class="form-control header-search-wrapper js-chromeless-input-container">
      <div class="header-search-scope">This repository</div>
      <input type="text"
        class="form-control header-search-input js-site-search-focus js-site-search-field is-clearable"
        data-hotkey="s"
        name="q"
        placeholder="Search"
        aria-label="Search this repository"
        data-unscoped-placeholder="Search GitHub"
        data-scoped-placeholder="Search"
        tabindex="1"
        autocapitalize="off">
    </label>
</form></div>


      <ul class="header-nav left" role="navigation">
        <li class="header-nav-item">
          <a href="/pulls" class="js-selected-navigation-item header-nav-link" data-ga-click="Header, click, Nav menu - item:pulls context:user" data-hotkey="g p" data-selected-links="/pulls /pulls/assigned /pulls/mentioned /pulls">
            Pull requests
</a>        </li>
        <li class="header-nav-item">
          <a href="/issues" class="js-selected-navigation-item header-nav-link" data-ga-click="Header, click, Nav menu - item:issues context:user" data-hotkey="g i" data-selected-links="/issues /issues/assigned /issues/mentioned /issues">
            Issues
</a>        </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="https://gist.github.com/" data-ga-click="Header, go to gist, text:gist">Gist</a>
          </li>
      </ul>

    
<ul class="header-nav user-nav right" id="user-links">
  <li class="header-nav-item">
    
    <a href="/notifications" aria-label="You have unread notifications" class="header-nav-link notification-indicator tooltipped tooltipped-s js-socket-channel js-notification-indicator" data-channel="notification-changed-v2:8814406" data-ga-click="Header, go to notifications, icon:unread" data-hotkey="g n">
        <span class="mail-status unread"></span>
        <svg aria-hidden="true" class="octicon octicon-bell" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M14 12v1H0v-1l0.73-0.58c0.77-0.77 0.81-2.55 1.19-4.42 0.77-3.77 4.08-5 4.08-5 0-0.55 0.45-1 1-1s1 0.45 1 1c0 0 3.39 1.23 4.16 5 0.38 1.88 0.42 3.66 1.19 4.42l0.66 0.58z m-7 4c1.11 0 2-0.89 2-2H5c0 1.11 0.89 2 2 2z"></path></svg>
</a>
  </li>

  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link tooltipped tooltipped-s js-menu-target" href="/new"
       aria-label="Create new…"
       data-ga-click="Header, create new, icon:add">
      <svg aria-hidden="true" class="octicon octicon-plus left" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 9H7v5H5V9H0V7h5V2h2v5h5v2z"></path></svg>
      <span class="dropdown-caret"></span>
    </a>

    <div class="dropdown-menu-content js-menu-content">
      <ul class="dropdown-menu dropdown-menu-sw">
        
<a class="dropdown-item" href="/new" data-ga-click="Header, create new repository">
  New repository
</a>

  <a class="dropdown-item" href="/new/import" data-ga-click="Header, import a repository">
    Import repository
  </a>


  <a class="dropdown-item" href="/organizations/new" data-ga-click="Header, create new organization">
    New organization
  </a>

  <div class="dropdown-divider"></div>
  <div class="dropdown-header">
    <span title="Meta-Man">This organization</span>
  </div>
  <a class="dropdown-item" href="/orgs/Meta-Man/invitations/new" data-ga-click="Header, invite someone">
    Invite someone
  </a>
  <a class="dropdown-item" href="/orgs/Meta-Man/new-team" data-ga-click="Header, create new team">
    New team
  </a>
  <a class="dropdown-item" href="/organizations/Meta-Man/repositories/new" data-ga-click="Header, create new organization repository, icon:repo">
    New repository
  </a>


  <div class="dropdown-divider"></div>
  <div class="dropdown-header">
    <span title="Meta-Man/plyr">This repository</span>
  </div>
    <a class="dropdown-item" href="/Meta-Man/plyr/settings/collaboration" data-ga-click="Header, create new collaborator">
      New collaborator
    </a>

      </ul>
    </div>
  </li>

  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link name tooltipped tooltipped-sw js-menu-target" href="/SpootDev"
       aria-label="View profile and more"
       data-ga-click="Header, show menu, icon:avatar">
      <img alt="@SpootDev" class="avatar" height="20" src="https://avatars3.githubusercontent.com/u/8814406?v=3&amp;s=40" width="20" />
      <span class="dropdown-caret"></span>
    </a>

    <div class="dropdown-menu-content js-menu-content">
      <div class="dropdown-menu  dropdown-menu-sw">
        <div class=" dropdown-header header-nav-current-user css-truncate">
            Signed in as <strong class="css-truncate-target">SpootDev</strong>

        </div>


        <div class="dropdown-divider"></div>

          <a class="dropdown-item" href="/SpootDev" data-ga-click="Header, go to profile, text:your profile">
            Your profile
          </a>
        <a class="dropdown-item" href="/stars" data-ga-click="Header, go to starred repos, text:your stars">
          Your stars
        </a>
          <a class="dropdown-item" href="/explore" data-ga-click="Header, go to explore, text:explore">
            Explore
          </a>
          <a class="dropdown-item" href="/integrations" data-ga-click="Header, go to integrations, text:integrations">
            Integrations
          </a>
        <a class="dropdown-item" href="https://help.github.com" data-ga-click="Header, go to help, text:help">
          Help
        </a>


          <div class="dropdown-divider"></div>

          <a class="dropdown-item" href="/settings/profile" data-ga-click="Header, go to settings, icon:settings">
            Settings
          </a>

          <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/logout" class="logout-form" data-form-nonce="f39c2a21a02fc39998e19fa7e5c58cfe76ce9a4b" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="qGwi4f9UMvJINaMx5jr1M0KipZR4ZGF3NOxNHfhrXHVaQJMfFuMvwPqk4J2aY5cjLAn46sWJ/5+UE7/fZBRwmQ==" /></div>
            <button class="dropdown-item dropdown-signout" data-ga-click="Header, sign out, icon:logout">
              Sign out
            </button>
</form>
      </div>
    </div>
  </li>
</ul>


    
  </div>
</div>


      


    <div id="start-of-content" class="accessibility-aid"></div>

      <div id="js-flash-container">
</div>


    <div role="main" class="main-content">
        <div itemscope itemtype="http://schema.org/SoftwareSourceCode">
    <div id="js-repo-pjax-container" data-pjax-container>
      
<div class="pagehead repohead instapaper_ignore readability-menu experiment-repo-nav">
  <div class="container repohead-details-container">

    

<ul class="pagehead-actions">

  <li>
        <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/notifications/subscribe" class="js-social-container" data-autosubmit="true" data-form-nonce="f39c2a21a02fc39998e19fa7e5c58cfe76ce9a4b" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="YZjYmsd/zLfiUtsrfewvtUxhxw4T2AYpDtJ3QFYRAEGdq7UMctBpolr6Iix3pWptxIWXvXCudQV245zipL4t6w==" /></div>      <input class="form-control" id="repository_id" name="repository_id" type="hidden" value="59605832" />

        <div class="select-menu js-menu-container js-select-menu">
          <a href="/Meta-Man/plyr/subscription"
            class="btn btn-sm btn-with-count select-menu-button js-menu-target" role="button" tabindex="0" aria-haspopup="true"
            data-ga-click="Repository, click Watch settings, action:blob#show">
            <span class="js-select-button">
              <svg aria-hidden="true" class="octicon octicon-eye" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M8.06 2C3 2 0 8 0 8s3 6 8.06 6c4.94 0 7.94-6 7.94-6S13 2 8.06 2z m-0.06 10c-2.2 0-4-1.78-4-4 0-2.2 1.8-4 4-4 2.22 0 4 1.8 4 4 0 2.22-1.78 4-4 4z m2-4c0 1.11-0.89 2-2 2s-2-0.89-2-2 0.89-2 2-2 2 0.89 2 2z"></path></svg>
              Unwatch
            </span>
          </a>
          <a class="social-count js-social-count" href="/Meta-Man/plyr/watchers">
            1
          </a>

        <div class="select-menu-modal-holder">
          <div class="select-menu-modal subscription-menu-modal js-menu-content" aria-hidden="true">
            <div class="select-menu-header js-navigation-enable" tabindex="-1">
              <svg aria-label="Close" class="octicon octicon-x js-menu-close" height="16" role="img" version="1.1" viewBox="0 0 12 16" width="12"><path d="M7.48 8l3.75 3.75-1.48 1.48-3.75-3.75-3.75 3.75-1.48-1.48 3.75-3.75L0.77 4.25l1.48-1.48 3.75 3.75 3.75-3.75 1.48 1.48-3.75 3.75z"></path></svg>
              <span class="select-menu-title">Notifications</span>
            </div>

              <div class="select-menu-list js-navigation-container" role="menu">

                <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                  <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
                  <div class="select-menu-item-text">
                    <input id="do_included" name="do" type="radio" value="included" />
                    <span class="select-menu-item-heading">Not watching</span>
                    <span class="description">Be notified when participating or @mentioned.</span>
                    <span class="js-select-button-text hidden-select-button-text">
                      <svg aria-hidden="true" class="octicon octicon-eye" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M8.06 2C3 2 0 8 0 8s3 6 8.06 6c4.94 0 7.94-6 7.94-6S13 2 8.06 2z m-0.06 10c-2.2 0-4-1.78-4-4 0-2.2 1.8-4 4-4 2.22 0 4 1.8 4 4 0 2.22-1.78 4-4 4z m2-4c0 1.11-0.89 2-2 2s-2-0.89-2-2 0.89-2 2-2 2 0.89 2 2z"></path></svg>
                      Watch
                    </span>
                  </div>
                </div>

                <div class="select-menu-item js-navigation-item selected" role="menuitem" tabindex="0">
                  <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
                  <div class="select-menu-item-text">
                    <input checked="checked" id="do_subscribed" name="do" type="radio" value="subscribed" />
                    <span class="select-menu-item-heading">Watching</span>
                    <span class="description">Be notified of all conversations.</span>
                    <span class="js-select-button-text hidden-select-button-text">
                      <svg aria-hidden="true" class="octicon octicon-eye" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M8.06 2C3 2 0 8 0 8s3 6 8.06 6c4.94 0 7.94-6 7.94-6S13 2 8.06 2z m-0.06 10c-2.2 0-4-1.78-4-4 0-2.2 1.8-4 4-4 2.22 0 4 1.8 4 4 0 2.22-1.78 4-4 4z m2-4c0 1.11-0.89 2-2 2s-2-0.89-2-2 0.89-2 2-2 2 0.89 2 2z"></path></svg>
                      Unwatch
                    </span>
                  </div>
                </div>

                <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                  <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
                  <div class="select-menu-item-text">
                    <input id="do_ignore" name="do" type="radio" value="ignore" />
                    <span class="select-menu-item-heading">Ignoring</span>
                    <span class="description">Never be notified.</span>
                    <span class="js-select-button-text hidden-select-button-text">
                      <svg aria-hidden="true" class="octicon octicon-mute" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M8 2.81v10.38c0 0.67-0.81 1-1.28 0.53L3 10H1c-0.55 0-1-0.45-1-1V7c0-0.55 0.45-1 1-1h2l3.72-3.72c0.47-0.47 1.28-0.14 1.28 0.53z m7.53 3.22l-1.06-1.06-1.97 1.97-1.97-1.97-1.06 1.06 1.97 1.97-1.97 1.97 1.06 1.06 1.97-1.97 1.97 1.97 1.06-1.06-1.97-1.97 1.97-1.97z"></path></svg>
                      Stop ignoring
                    </span>
                  </div>
                </div>

              </div>

            </div>
          </div>
        </div>
</form>
  </li>

  <li>
    
  <div class="js-toggler-container js-social-container starring-container ">

    <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/Meta-Man/plyr/unstar" class="starred" data-form-nonce="f39c2a21a02fc39998e19fa7e5c58cfe76ce9a4b" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="TRP5CSvR3cboEOi/f1GJQM9xKahzGrjcE6JC6hbcY2+mekpKXCnsJBGVO3M0GL2EvID/xzEu/M4kHrDyjHhOPQ==" /></div>
      <button
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Unstar this repository" title="Unstar Meta-Man/plyr"
        data-ga-click="Repository, click unstar button, action:blob#show; text:Unstar">
        <svg aria-hidden="true" class="octicon octicon-star" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M14 6l-4.9-0.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14l4.33-2.33 4.33 2.33L10.4 9.26 14 6z"></path></svg>
        Unstar
      </button>
        <a class="social-count js-social-count" href="/Meta-Man/plyr/stargazers">
          0
        </a>
</form>
    <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/Meta-Man/plyr/star" class="unstarred" data-form-nonce="f39c2a21a02fc39998e19fa7e5c58cfe76ce9a4b" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="9fzY44IYRgJj08sUdEDtVuU2UfZh3gft9tIqA9xkOie0u9rZ7hOvCF+qqdYXgOU+2Qct+E6c7gbPF5impXArFg==" /></div>
      <button
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Star this repository" title="Star Meta-Man/plyr"
        data-ga-click="Repository, click star button, action:blob#show; text:Star">
        <svg aria-hidden="true" class="octicon octicon-star" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M14 6l-4.9-0.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14l4.33-2.33 4.33 2.33L10.4 9.26 14 6z"></path></svg>
        Star
      </button>
        <a class="social-count js-social-count" href="/Meta-Man/plyr/stargazers">
          0
        </a>
</form>  </div>

  </li>

  <li>
          <a href="#fork-destination-box" class="btn btn-sm btn-with-count"
              title="Fork your own copy of Meta-Man/plyr to your account"
              aria-label="Fork your own copy of Meta-Man/plyr to your account"
              rel="facebox"
              data-ga-click="Repository, show fork modal, action:blob#show; text:Fork">
              <svg aria-hidden="true" class="octicon octicon-repo-forked" height="16" version="1.1" viewBox="0 0 10 16" width="10"><path d="M8 1c-1.11 0-2 0.89-2 2 0 0.73 0.41 1.38 1 1.72v1.28L5 8 3 6v-1.28c0.59-0.34 1-0.98 1-1.72 0-1.11-0.89-2-2-2S0 1.89 0 3c0 0.73 0.41 1.38 1 1.72v1.78l3 3v1.78c-0.59 0.34-1 0.98-1 1.72 0 1.11 0.89 2 2 2s2-0.89 2-2c0-0.73-0.41-1.38-1-1.72V9.5l3-3V4.72c0.59-0.34 1-0.98 1-1.72 0-1.11-0.89-2-2-2zM2 4.2c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z m3 10c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z m3-10c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z"></path></svg>
            Fork
          </a>

          <div id="fork-destination-box" style="display: none;">
            <h2 class="facebox-header" data-facebox-id="facebox-header">Where should we fork this repository?</h2>
            <include-fragment src=""
                class="js-fork-select-fragment fork-select-fragment"
                data-url="/Meta-Man/plyr/fork?fragment=1">
              <img alt="Loading" height="64" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-128.gif" width="64" />
            </include-fragment>
          </div>

    <a href="/Meta-Man/plyr/network" class="social-count">
      499
    </a>
  </li>
</ul>

    <h1 class="entry-title public ">
  <svg aria-hidden="true" class="octicon octicon-repo-forked" height="16" version="1.1" viewBox="0 0 10 16" width="10"><path d="M8 1c-1.11 0-2 0.89-2 2 0 0.73 0.41 1.38 1 1.72v1.28L5 8 3 6v-1.28c0.59-0.34 1-0.98 1-1.72 0-1.11-0.89-2-2-2S0 1.89 0 3c0 0.73 0.41 1.38 1 1.72v1.78l3 3v1.78c-0.59 0.34-1 0.98-1 1.72 0 1.11 0.89 2 2 2s2-0.89 2-2c0-0.73-0.41-1.38-1-1.72V9.5l3-3V4.72c0.59-0.34 1-0.98 1-1.72 0-1.11-0.89-2-2-2zM2 4.2c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z m3 10c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z m3-10c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z"></path></svg>
  <span class="author" itemprop="author"><a href="/Meta-Man" class="url fn" rel="author">Meta-Man</a></span><!--
--><span class="path-divider">/</span><!--
--><strong itemprop="name"><a href="/Meta-Man/plyr" data-pjax="#js-repo-pjax-container">plyr</a></strong>

    <span class="fork-flag">
      <span class="text">forked from <a href="/Selz/plyr">Selz/plyr</a></span>
    </span>
</h1>

  </div>
  <div class="container">
    
<nav class="reponav js-repo-nav js-sidenav-container-pjax"
     itemscope
     itemtype="http://schema.org/BreadcrumbList"
     role="navigation"
     data-pjax="#js-repo-pjax-container">

  <span itemscope itemtype="http://schema.org/ListItem" itemprop="itemListElement">
    <a href="/Meta-Man/plyr" aria-selected="true" class="js-selected-navigation-item selected reponav-item" data-hotkey="g c" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /Meta-Man/plyr" itemprop="url">
      <svg aria-hidden="true" class="octicon octicon-code" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M9.5 3l-1.5 1.5 3.5 3.5L8 11.5l1.5 1.5 4.5-5L9.5 3zM4.5 3L0 8l4.5 5 1.5-1.5L2.5 8l3.5-3.5L4.5 3z"></path></svg>
      <span itemprop="name">Code</span>
      <meta itemprop="position" content="1">
</a>  </span>


  <span itemscope itemtype="http://schema.org/ListItem" itemprop="itemListElement">
    <a href="/Meta-Man/plyr/pulls" class="js-selected-navigation-item reponav-item" data-hotkey="g p" data-selected-links="repo_pulls /Meta-Man/plyr/pulls" itemprop="url">
      <svg aria-hidden="true" class="octicon octicon-git-pull-request" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M11 11.28c0-1.73 0-6.28 0-6.28-0.03-0.78-0.34-1.47-0.94-2.06s-1.28-0.91-2.06-0.94c0 0-1.02 0-1 0V0L4 3l3 3V4h1c0.27 0.02 0.48 0.11 0.69 0.31s0.3 0.42 0.31 0.69v6.28c-0.59 0.34-1 0.98-1 1.72 0 1.11 0.89 2 2 2s2-0.89 2-2c0-0.73-0.41-1.38-1-1.72z m-1 2.92c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2zM4 3c0-1.11-0.89-2-2-2S0 1.89 0 3c0 0.73 0.41 1.38 1 1.72 0 1.55 0 5.56 0 6.56-0.59 0.34-1 0.98-1 1.72 0 1.11 0.89 2 2 2s2-0.89 2-2c0-0.73-0.41-1.38-1-1.72V4.72c0.59-0.34 1-0.98 1-1.72z m-0.8 10c0 0.66-0.55 1.2-1.2 1.2s-1.2-0.55-1.2-1.2 0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2z m-1.2-8.8c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z"></path></svg>
      <span itemprop="name">Pull requests</span>
      <span class="counter">0</span>
      <meta itemprop="position" content="3">
</a>  </span>

    <a href="/Meta-Man/plyr/wiki" class="js-selected-navigation-item reponav-item" data-hotkey="g w" data-selected-links="repo_wiki /Meta-Man/plyr/wiki">
      <svg aria-hidden="true" class="octicon octicon-book" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M2 5h4v1H2v-1z m0 3h4v-1H2v1z m0 2h4v-1H2v1z m11-5H9v1h4v-1z m0 2H9v1h4v-1z m0 2H9v1h4v-1z m2-6v9c0 0.55-0.45 1-1 1H8.5l-1 1-1-1H1c-0.55 0-1-0.45-1-1V3c0-0.55 0.45-1 1-1h5.5l1 1 1-1h5.5c0.55 0 1 0.45 1 1z m-8 0.5l-0.5-0.5H1v9h6V3.5z m7-0.5H8.5l-0.5 0.5v8.5h6V3z"></path></svg>
      Wiki
</a>

  <a href="/Meta-Man/plyr/pulse" class="js-selected-navigation-item reponav-item" data-selected-links="pulse /Meta-Man/plyr/pulse">
    <svg aria-hidden="true" class="octicon octicon-pulse" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M11.5 8L8.8 5.4 6.6 8.5 5.5 1.6 2.38 8H0V10h3.6L4.5 8.2l0.9 5.4L9 8.5l1.6 1.5H14V8H11.5z"></path></svg>
    Pulse
</a>
  <a href="/Meta-Man/plyr/graphs" class="js-selected-navigation-item reponav-item" data-selected-links="repo_graphs repo_contributors /Meta-Man/plyr/graphs">
    <svg aria-hidden="true" class="octicon octicon-graph" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M16 14v1H0V0h1v14h15z m-11-1H3V8h2v5z m4 0H7V3h2v10z m4 0H11V6h2v7z"></path></svg>
    Graphs
</a>
    <a href="/Meta-Man/plyr/settings" class="js-selected-navigation-item reponav-item" data-selected-links="repo_settings repo_branch_settings hooks /Meta-Man/plyr/settings">
      <svg aria-hidden="true" class="octicon octicon-gear" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M14 8.77V7.17l-1.94-0.64-0.45-1.09 0.88-1.84-1.13-1.13-1.81 0.91-1.09-0.45-0.69-1.92H6.17l-0.63 1.94-1.11 0.45-1.84-0.88-1.13 1.13 0.91 1.81-0.45 1.09L0 7.23v1.59l1.94 0.64 0.45 1.09-0.88 1.84 1.13 1.13 1.81-0.91 1.09 0.45 0.69 1.92h1.59l0.63-1.94 1.11-0.45 1.84 0.88 1.13-1.13-0.92-1.81 0.47-1.09 1.92-0.69zM7 11c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3z"></path></svg>
      Settings
</a>
</nav>

  </div>
</div>

<div class="container new-discussion-timeline experiment-repo-nav">
  <div class="repository-content">

    

<a href="/Meta-Man/plyr/blob/351e1540c5e7241bc7c4a2d0a0598620c1699d73/dist/plyr.js" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

<!-- blob contrib key: blob_contributors:v21:295a1212eeed1f329c49ec3a64faa656 -->

<div class="file-navigation js-zeroclipboard-container">
  
<div class="select-menu branch-select-menu js-menu-container js-select-menu left">
  <button class="btn btn-sm select-menu-button js-menu-target css-truncate" data-hotkey="w"
    title="master"
    type="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <i>Branch:</i>
    <span class="js-select-button css-truncate-target">master</span>
  </button>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <svg aria-label="Close" class="octicon octicon-x js-menu-close" height="16" role="img" version="1.1" viewBox="0 0 12 16" width="12"><path d="M7.48 8l3.75 3.75-1.48 1.48-3.75-3.75-3.75 3.75-1.48-1.48 3.75-3.75L0.77 4.25l1.48-1.48 3.75 3.75 3.75-3.75 1.48 1.48-3.75 3.75z"></path></svg>
        <span class="select-menu-title">Switch branches/tags</span>
      </div>

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Find or create a branch…" id="context-commitish-filter-field" class="form-control js-filterable-field js-navigation-enable" placeholder="Find or create a branch…">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" data-filter-placeholder="Find or create a branch…" class="js-select-menu-tab" role="tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" data-filter-placeholder="Find a tag…" class="js-select-menu-tab" role="tab">Tags</a>
            </li>
          </ul>
        </div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches" role="menu">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/Meta-Man/plyr/blob/develop/dist/plyr.js"
               data-name="develop"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text" title="develop">
                develop
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open selected"
               href="/Meta-Man/plyr/blob/master/dist/plyr.js"
               data-name="master"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text" title="master">
                master
              </span>
            </a>
        </div>

          <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/Meta-Man/plyr/branches" class="js-create-branch select-menu-item select-menu-new-item-form js-navigation-item js-new-item-form" data-form-nonce="f39c2a21a02fc39998e19fa7e5c58cfe76ce9a4b" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="RlSNaOVgGx0ypevT/IeMzD3icrpeIwFFkC27L5kmz+DYPFsnOw/3qNqPRIACj5XeJVloVBA74IK/wNt2di0f/w==" /></div>
          <svg aria-hidden="true" class="octicon octicon-git-branch select-menu-item-icon" height="16" version="1.1" viewBox="0 0 10 16" width="10"><path d="M10 5c0-1.11-0.89-2-2-2s-2 0.89-2 2c0 0.73 0.41 1.38 1 1.72v0.3c-0.02 0.52-0.23 0.98-0.63 1.38s-0.86 0.61-1.38 0.63c-0.83 0.02-1.48 0.16-2 0.45V4.72c0.59-0.34 1-0.98 1-1.72 0-1.11-0.89-2-2-2S0 1.89 0 3c0 0.73 0.41 1.38 1 1.72v6.56C0.41 11.63 0 12.27 0 13c0 1.11 0.89 2 2 2s2-0.89 2-2c0-0.53-0.2-1-0.53-1.36 0.09-0.06 0.48-0.41 0.59-0.47 0.25-0.11 0.56-0.17 0.94-0.17 1.05-0.05 1.95-0.45 2.75-1.25s1.2-1.98 1.25-3.02h-0.02c0.61-0.36 1.02-1 1.02-1.73zM2 1.8c0.66 0 1.2 0.55 1.2 1.2s-0.55 1.2-1.2 1.2-1.2-0.55-1.2-1.2 0.55-1.2 1.2-1.2z m0 12.41c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z m6-8c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z"></path></svg>
            <div class="select-menu-item-text">
              <span class="select-menu-item-heading">Create branch: <span class="js-new-item-name"></span></span>
              <span class="description">from ‘master’</span>
            </div>
            <input type="hidden" name="name" id="name" class="js-new-item-value">
            <input type="hidden" name="branch" id="branch" value="master">
            <input type="hidden" name="path" id="path" value="dist/plyr.js">
</form>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.16/dist/plyr.js"
              data-name="v1.6.16"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.16">
                v1.6.16
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.15/dist/plyr.js"
              data-name="v1.6.15"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.15">
                v1.6.15
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.14/dist/plyr.js"
              data-name="v1.6.14"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.14">
                v1.6.14
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.13/dist/plyr.js"
              data-name="v1.6.13"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.13">
                v1.6.13
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.12/dist/plyr.js"
              data-name="v1.6.12"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.12">
                v1.6.12
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.11/dist/plyr.js"
              data-name="v1.6.11"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.11">
                v1.6.11
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.10/dist/plyr.js"
              data-name="v1.6.10"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.10">
                v1.6.10
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.9/dist/plyr.js"
              data-name="v1.6.9"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.9">
                v1.6.9
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.8/dist/plyr.js"
              data-name="v1.6.8"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.8">
                v1.6.8
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.7/dist/plyr.js"
              data-name="v1.6.7"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.7">
                v1.6.7
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.6/dist/plyr.js"
              data-name="v1.6.6"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.6">
                v1.6.6
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.5/dist/plyr.js"
              data-name="v1.6.5"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.5">
                v1.6.5
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.4/dist/plyr.js"
              data-name="v1.6.4"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.4">
                v1.6.4
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.3/dist/plyr.js"
              data-name="v1.6.3"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.3">
                v1.6.3
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.2/dist/plyr.js"
              data-name="v1.6.2"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.2">
                v1.6.2
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.1/dist/plyr.js"
              data-name="v1.6.1"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.1">
                v1.6.1
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.6.0/dist/plyr.js"
              data-name="v1.6.0"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.6.0">
                v1.6.0
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.21/dist/plyr.js"
              data-name="v1.5.21"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.21">
                v1.5.21
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.20/dist/plyr.js"
              data-name="v1.5.20"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.20">
                v1.5.20
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.19/dist/plyr.js"
              data-name="v1.5.19"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.19">
                v1.5.19
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.18/dist/plyr.js"
              data-name="v1.5.18"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.18">
                v1.5.18
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.17/dist/plyr.js"
              data-name="v1.5.17"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.17">
                v1.5.17
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.16/dist/plyr.js"
              data-name="v1.5.16"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.16">
                v1.5.16
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.15/dist/plyr.js"
              data-name="v1.5.15"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.15">
                v1.5.15
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.14/dist/plyr.js"
              data-name="v1.5.14"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.14">
                v1.5.14
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.13/dist/plyr.js"
              data-name="v1.5.13"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.13">
                v1.5.13
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.12/dist/plyr.js"
              data-name="v1.5.12"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.12">
                v1.5.12
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.11/dist/plyr.js"
              data-name="v1.5.11"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.11">
                v1.5.11
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.10/dist/plyr.js"
              data-name="v1.5.10"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.10">
                v1.5.10
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.9/dist/plyr.js"
              data-name="v1.5.9"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.9">
                v1.5.9
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.8/dist/plyr.js"
              data-name="v1.5.8"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.8">
                v1.5.8
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.7/dist/plyr.js"
              data-name="v1.5.7"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.7">
                v1.5.7
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.6/dist/plyr.js"
              data-name="v1.5.6"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.6">
                v1.5.6
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.5/dist/plyr.js"
              data-name="v1.5.5"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.5">
                v1.5.5
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.4/dist/plyr.js"
              data-name="v1.5.4"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.4">
                v1.5.4
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.3/dist/plyr.js"
              data-name="v1.5.3"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.3">
                v1.5.3
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.2/dist/plyr.js"
              data-name="v1.5.2"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.2">
                v1.5.2
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.1/dist/plyr.js"
              data-name="v1.5.1"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.1">
                v1.5.1
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.5.0/dist/plyr.js"
              data-name="v1.5.0"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.5.0">
                v1.5.0
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.3.7/dist/plyr.js"
              data-name="v1.3.7"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.3.7">
                v1.3.7
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.3.6/dist/plyr.js"
              data-name="v1.3.6"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.3.6">
                v1.3.6
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.3.5/dist/plyr.js"
              data-name="v1.3.5"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.3.5">
                v1.3.5
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.3.4/dist/plyr.js"
              data-name="v1.3.4"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.3.4">
                v1.3.4
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.3.3/dist/plyr.js"
              data-name="v1.3.3"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.3.3">
                v1.3.3
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.3.2/dist/plyr.js"
              data-name="v1.3.2"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.3.2">
                v1.3.2
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.3.1/dist/plyr.js"
              data-name="v1.3.1"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.3.1">
                v1.3.1
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.3.0/dist/plyr.js"
              data-name="v1.3.0"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.3.0">
                v1.3.0
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.2.6/dist/plyr.js"
              data-name="v1.2.6"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.2.6">
                v1.2.6
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.2.5/dist/plyr.js"
              data-name="v1.2.5"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.2.5">
                v1.2.5
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.2.4/dist/plyr.js"
              data-name="v1.2.4"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.2.4">
                v1.2.4
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.2.3/dist/plyr.js"
              data-name="v1.2.3"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.2.3">
                v1.2.3
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.2.2/dist/plyr.js"
              data-name="v1.2.2"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.2.2">
                v1.2.2
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.2.1/dist/plyr.js"
              data-name="v1.2.1"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.2.1">
                v1.2.1
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.2.0/dist/plyr.js"
              data-name="v1.2.0"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.2.0">
                v1.2.0
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.14/dist/plyr.js"
              data-name="v1.1.14"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.14">
                v1.1.14
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.13/dist/plyr.js"
              data-name="v1.1.13"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.13">
                v1.1.13
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.12/dist/plyr.js"
              data-name="v1.1.12"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.12">
                v1.1.12
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.11/dist/plyr.js"
              data-name="v1.1.11"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.11">
                v1.1.11
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.10/dist/plyr.js"
              data-name="v1.1.10"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.10">
                v1.1.10
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.9/dist/plyr.js"
              data-name="v1.1.9"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.9">
                v1.1.9
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.8/dist/plyr.js"
              data-name="v1.1.8"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.8">
                v1.1.8
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.7/dist/plyr.js"
              data-name="v1.1.7"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.7">
                v1.1.7
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.6/dist/plyr.js"
              data-name="v1.1.6"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.6">
                v1.1.6
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.5/dist/plyr.js"
              data-name="v1.1.5"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.5">
                v1.1.5
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.4/dist/plyr.js"
              data-name="v1.1.4"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.4">
                v1.1.4
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.3/dist/plyr.js"
              data-name="v1.1.3"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.3">
                v1.1.3
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.2/dist/plyr.js"
              data-name="v1.1.2"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.2">
                v1.1.2
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.1/dist/plyr.js"
              data-name="v1.1.1"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.1">
                v1.1.1
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.1.0/dist/plyr.js"
              data-name="v1.1.0"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.0">
                v1.1.0
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.31/dist/plyr.js"
              data-name="v1.0.31"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.31">
                v1.0.31
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.30/dist/plyr.js"
              data-name="v1.0.30"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.30">
                v1.0.30
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.29/dist/plyr.js"
              data-name="v1.0.29"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.29">
                v1.0.29
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.28/dist/plyr.js"
              data-name="v1.0.28"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.28">
                v1.0.28
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.27/dist/plyr.js"
              data-name="v1.0.27"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.27">
                v1.0.27
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.26/dist/plyr.js"
              data-name="v1.0.26"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.26">
                v1.0.26
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.25/dist/plyr.js"
              data-name="v1.0.25"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.25">
                v1.0.25
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.24/dist/plyr.js"
              data-name="v1.0.24"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.24">
                v1.0.24
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.23/dist/plyr.js"
              data-name="v1.0.23"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.23">
                v1.0.23
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.22/dist/plyr.js"
              data-name="v1.0.22"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.22">
                v1.0.22
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.21/dist/plyr.js"
              data-name="v1.0.21"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.21">
                v1.0.21
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.20/dist/plyr.js"
              data-name="v1.0.20"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.20">
                v1.0.20
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.19/dist/plyr.js"
              data-name="v1.0.19"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.19">
                v1.0.19
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.18/dist/plyr.js"
              data-name="v1.0.18"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.18">
                v1.0.18
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.17/dist/plyr.js"
              data-name="v1.0.17"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.17">
                v1.0.17
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.16/dist/plyr.js"
              data-name="v1.0.16"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.16">
                v1.0.16
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.15/dist/plyr.js"
              data-name="v1.0.15"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.15">
                v1.0.15
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.14/dist/plyr.js"
              data-name="v1.0.14"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.14">
                v1.0.14
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.13/dist/plyr.js"
              data-name="v1.0.13"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.13">
                v1.0.13
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.12/dist/plyr.js"
              data-name="v1.0.12"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.12">
                v1.0.12
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.11/dist/plyr.js"
              data-name="v1.0.11"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.11">
                v1.0.11
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.10/dist/plyr.js"
              data-name="v1.0.10"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.10">
                v1.0.10
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.9/dist/plyr.js"
              data-name="v1.0.9"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.9">
                v1.0.9
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.8/dist/plyr.js"
              data-name="v1.0.8"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.8">
                v1.0.8
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.7/dist/plyr.js"
              data-name="v1.0.7"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.7">
                v1.0.7
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.6/dist/plyr.js"
              data-name="v1.0.6"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.6">
                v1.0.6
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.5/dist/plyr.js"
              data-name="v1.0.5"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.5">
                v1.0.5
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.4/dist/plyr.js"
              data-name="v1.0.4"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.4">
                v1.0.4
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.3/dist/plyr.js"
              data-name="v1.0.3"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.3">
                v1.0.3
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.2/dist/plyr.js"
              data-name="v1.0.2"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.2">
                v1.0.2
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/Meta-Man/plyr/tree/v1.0.1/dist/plyr.js"
              data-name="v1.0.1"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0.1">
                v1.0.1
              </span>
            </a>
        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div>

    </div>
  </div>
</div>

  <div class="btn-group right">
    <a href="/Meta-Man/plyr/find/master"
          class="js-pjax-capture-input btn btn-sm"
          data-pjax
          data-hotkey="t">
      Find file
    </a>
    <button aria-label="Copy file path to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button">Copy path</button>
  </div>
  <div class="breadcrumb js-zeroclipboard-target">
    <span class="repo-root js-repo-root"><span class="js-path-segment"><a href="/Meta-Man/plyr"><span>plyr</span></a></span></span><span class="separator">/</span><span class="js-path-segment"><a href="/Meta-Man/plyr/tree/master/dist"><span>dist</span></a></span><span class="separator">/</span><strong class="final-path">plyr.js</strong>
  </div>
</div>

<include-fragment class="commit-tease" src="/Meta-Man/plyr/contributors/master/dist/plyr.js">
  <div>
    Fetching contributors&hellip;
  </div>

  <div class="commit-tease-contributors">
    <img alt="" class="loader-loading left" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32-EAF2F5.gif" width="16" />
    <span class="loader-error">Cannot retrieve contributors at this time</span>
  </div>
</include-fragment>
<div class="file">
  <div class="file-header">
  <div class="file-actions">

    <div class="btn-group">
      <a href="/Meta-Man/plyr/raw/master/dist/plyr.js" class="btn btn-sm " id="raw-url">Raw</a>
        <a href="/Meta-Man/plyr/blame/master/dist/plyr.js" class="btn btn-sm js-update-url-with-hash">Blame</a>
      <a href="/Meta-Man/plyr/commits/master/dist/plyr.js" class="btn btn-sm " rel="nofollow">History</a>
    </div>


        <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/Meta-Man/plyr/edit/master/dist/plyr.js" class="inline-form js-update-url-with-hash" data-form-nonce="f39c2a21a02fc39998e19fa7e5c58cfe76ce9a4b" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="lKvl3CDcITxkcso5b2vUDnlBycA3kGTIPkudc53KZq1wCB61hQQKGstGqlXY74zCaLuXpHtRM3l4gOLZQ5oNyw==" /></div>
          <button class="btn-octicon tooltipped tooltipped-nw" type="submit"
            aria-label="Edit this file" data-hotkey="e" data-disable-with>
            <svg aria-hidden="true" class="octicon octicon-pencil" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M0 12v3h3l8-8-3-3L0 12z m3 2H1V12h1v1h1v1z m10.3-9.3l-1.3 1.3-3-3 1.3-1.3c0.39-0.39 1.02-0.39 1.41 0l1.59 1.59c0.39 0.39 0.39 1.02 0 1.41z"></path></svg>
          </button>
</form>        <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/Meta-Man/plyr/delete/master/dist/plyr.js" class="inline-form" data-form-nonce="f39c2a21a02fc39998e19fa7e5c58cfe76ce9a4b" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="aoXSBVDIq9x6gH9PaY8tiaD9VTGF+9fKgEv1aDR+b8YZD7uR5dXoBOmGqnimHlp+E1WYfj4YsVMRlWI2Z0AgDw==" /></div>
          <button class="btn-octicon btn-octicon-danger tooltipped tooltipped-nw" type="submit"
            aria-label="Delete this file" data-disable-with>
            <svg aria-hidden="true" class="octicon octicon-trashcan" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M10 2H8c0-0.55-0.45-1-1-1H4c-0.55 0-1 0.45-1 1H1c-0.55 0-1 0.45-1 1v1c0 0.55 0.45 1 1 1v9c0 0.55 0.45 1 1 1h7c0.55 0 1-0.45 1-1V5c0.55 0 1-0.45 1-1v-1c0-0.55-0.45-1-1-1z m-1 12H2V5h1v8h1V5h1v8h1V5h1v8h1V5h1v9z m1-10H1v-1h9v1z"></path></svg>
          </button>
</form>  </div>

  <div class="file-info">
      2 lines (2 sloc)
      <span class="file-info-divider"></span>
    38.4 KB
  </div>
</div>

  

  <div itemprop="text" class="blob-wrapper data type-javascript">
      <table class="highlight tab-size js-file-line-container" data-tab-size="8">
      <tr>
        <td id="L1" class="blob-num js-line-number" data-line-number="1"></td>
        <td id="LC1" class="blob-code blob-code-inner js-file-line">!function(e,t){&quot;use strict&quot;;&quot;object&quot;==typeof module&amp;&amp;&quot;object&quot;==typeof module.exports?module.exports=t(e,document):&quot;function&quot;==typeof define&amp;&amp;define.amd?define(null,function(){t(e,document)}):e.plyr=t(e,document)}(&quot;undefined&quot;!=typeof window?window:this,function(e,t){&quot;use strict&quot;;function n(){var e,n,a,r=navigator.userAgent,s=navigator.appName,o=&quot;&quot;+parseFloat(navigator.appVersion),i=parseInt(navigator.appVersion,10);return-1!==navigator.appVersion.indexOf(&quot;Windows NT&quot;)&amp;&amp;-1!==navigator.appVersion.indexOf(&quot;rv:11&quot;)?(s=&quot;IE&quot;,o=&quot;11;&quot;):-1!==(n=r.indexOf(&quot;MSIE&quot;))?(s=&quot;IE&quot;,o=r.substring(n+5)):-1!==(n=r.indexOf(&quot;Chrome&quot;))?(s=&quot;Chrome&quot;,o=r.substring(n+7)):-1!==(n=r.indexOf(&quot;Safari&quot;))?(s=&quot;Safari&quot;,o=r.substring(n+7),-1!==(n=r.indexOf(&quot;Version&quot;))&amp;&amp;(o=r.substring(n+8))):-1!==(n=r.indexOf(&quot;Firefox&quot;))?(s=&quot;Firefox&quot;,o=r.substring(n+8)):(e=r.lastIndexOf(&quot; &quot;)+1)&lt;(n=r.lastIndexOf(&quot;/&quot;))&amp;&amp;(s=r.substring(e,n),o=r.substring(n+1),s.toLowerCase()==s.toUpperCase()&amp;&amp;(s=navigator.appName)),-1!==(a=o.indexOf(&quot;;&quot;))&amp;&amp;(o=o.substring(0,a)),-1!==(a=o.indexOf(&quot; &quot;))&amp;&amp;(o=o.substring(0,a)),i=parseInt(&quot;&quot;+o,10),isNaN(i)&amp;&amp;(o=&quot;&quot;+parseFloat(navigator.appVersion),i=parseInt(navigator.appVersion,10)),{name:s,version:i,ios:/(iPad|iPhone|iPod)/g.test(navigator.platform),touch:&quot;ontouchstart&quot;in t.documentElement}}function a(e,t){var n=e.media;if(&quot;video&quot;==e.type)switch(t){case&quot;video/webm&quot;:return!(!n.canPlayType||!n.canPlayType(&#39;video/webm; codecs=&quot;vp8, vorbis&quot;&#39;).replace(/no/,&quot;&quot;));case&quot;video/mp4&quot;:return!(!n.canPlayType||!n.canPlayType(&#39;video/mp4; codecs=&quot;avc1.42E01E, mp4a.40.2&quot;&#39;).replace(/no/,&quot;&quot;));case&quot;video/ogg&quot;:return!(!n.canPlayType||!n.canPlayType(&#39;video/ogg; codecs=&quot;theora&quot;&#39;).replace(/no/,&quot;&quot;))}else if(&quot;audio&quot;==e.type)switch(t){case&quot;audio/mpeg&quot;:return!(!n.canPlayType||!n.canPlayType(&quot;audio/mpeg;&quot;).replace(/no/,&quot;&quot;));case&quot;audio/ogg&quot;:return!(!n.canPlayType||!n.canPlayType(&#39;audio/ogg; codecs=&quot;vorbis&quot;&#39;).replace(/no/,&quot;&quot;));case&quot;audio/wav&quot;:return!(!n.canPlayType||!n.canPlayType(&#39;audio/wav; codecs=&quot;1&quot;&#39;).replace(/no/,&quot;&quot;))}return!1}function r(e){if(!t.querySelectorAll(&#39;script[src=&quot;&#39;+e+&#39;&quot;]&#39;).length){var n=t.createElement(&quot;script&quot;);n.src=e;var a=t.getElementsByTagName(&quot;script&quot;)[0];a.parentNode.insertBefore(n,a)}}function s(e,t){return Array.prototype.indexOf&amp;&amp;-1!=e.indexOf(t)}function o(e,t,n){return e.replace(new RegExp(t.replace(/([.*+?\^=!:${}()|\[\]\/\\])/g,&quot;\\$1&quot;),&quot;g&quot;),n)}function i(e,t){e.length||(e=[e]);for(var n=e.length-1;n&gt;=0;n--){var a=n&gt;0?t.cloneNode(!0):t,r=e[n],s=r.parentNode,o=r.nextSibling;a.appendChild(r),o?s.insertBefore(a,o):s.appendChild(a)}}function l(e){for(var t=e.parentNode;e.firstChild;)t.insertBefore(e.firstChild,e);t.removeChild(e)}function u(e){e&amp;&amp;e.parentNode.removeChild(e)}function c(e,t){e.insertBefore(t,e.firstChild)}function p(e,t){for(var n in t)e.setAttribute(n,&quot;boolean&quot;==typeof t[n]&amp;&amp;t[n]?&quot;&quot;:t[n])}function d(e,n,a){var r=t.createElement(e);p(r,a),c(n,r)}function A(e){return e.replace(&quot;.&quot;,&quot;&quot;)}function m(e,t,n){if(e)if(e.classList)e.classList[n?&quot;add&quot;:&quot;remove&quot;](t);else{var a=(&quot; &quot;+e.className+&quot; &quot;).replace(/\s+/g,&quot; &quot;).replace(&quot; &quot;+t+&quot; &quot;,&quot;&quot;);e.className=a+(n?&quot; &quot;+t:&quot;&quot;)}}function f(e,t){return e?e.classList?e.classList.contains(t):new RegExp(&quot;(\\s|^)&quot;+t+&quot;(\\s|$)&quot;).test(e.className):!1}function y(e,t,n,a){e&amp;&amp;g(e,t,n,!0,a)}function b(e,t,n,a){e&amp;&amp;g(e,t,n,!1,a)}function v(e,t,n,a,r){y(e,t,function(t){n&amp;&amp;n.apply(e,[t]),a.apply(e,[t])},r)}function g(e,t,n,a,r){var s=t.split(&quot; &quot;);if(&quot;boolean&quot;!=typeof r&amp;&amp;(r=!1),e instanceof NodeList)for(var o=0;o&lt;e.length;o++)e[o]instanceof Node&amp;&amp;g(e[o],arguments[1],arguments[2],arguments[3]);else for(var i=0;i&lt;s.length;i++)e[a?&quot;addEventListener&quot;:&quot;removeEventListener&quot;](s[i],n,r)}function h(e,t,n,a){if(e&amp;&amp;t){&quot;boolean&quot;!=typeof n&amp;&amp;(n=!1);var r=new CustomEvent(t,{bubbles:n,detail:a});e.dispatchEvent(r)}}function k(e,t){return e?(t=&quot;boolean&quot;==typeof t?t:!e.getAttribute(&quot;aria-pressed&quot;),e.setAttribute(&quot;aria-pressed&quot;,t),t):void 0}function w(e,t){return 0===e||0===t||isNaN(e)||isNaN(t)?0:(e/t*100).toFixed(2)}function x(){var e=arguments;if(e.length){if(1==e.lenth)return e[0];for(var t=Array.prototype.shift.call(e),n=e.length,a=0;n&gt;a;a++){var r=e[a];for(var s in r)r[s]&amp;&amp;r[s].constructor&amp;&amp;r[s].constructor===Object?(t[s]=t[s]||{},x(t[s],r[s])):t[s]=r[s]}return t}}function T(){var e={supportsFullScreen:!1,isFullScreen:function(){return!1},requestFullScreen:function(){},cancelFullScreen:function(){},fullScreenEventName:&quot;&quot;,element:null,prefix:&quot;&quot;},n=&quot;webkit moz o ms khtml&quot;.split(&quot; &quot;);if(&quot;undefined&quot;!=typeof t.cancelFullScreen)e.supportsFullScreen=!0;else for(var a=0,r=n.length;r&gt;a;a++){if(e.prefix=n[a],&quot;undefined&quot;!=typeof t[e.prefix+&quot;CancelFullScreen&quot;]){e.supportsFullScreen=!0;break}if(&quot;undefined&quot;!=typeof t.msExitFullscreen&amp;&amp;t.msFullscreenEnabled){e.prefix=&quot;ms&quot;,e.supportsFullScreen=!0;break}}return e.supportsFullScreen&amp;&amp;(e.fullScreenEventName=&quot;ms&quot;==e.prefix?&quot;MSFullscreenChange&quot;:e.prefix+&quot;fullscreenchange&quot;,e.isFullScreen=function(e){switch(&quot;undefined&quot;==typeof e&amp;&amp;(e=t.body),this.prefix){case&quot;&quot;:return t.fullscreenElement==e;case&quot;moz&quot;:return t.mozFullScreenElement==e;default:return t[this.prefix+&quot;FullscreenElement&quot;]==e}},e.requestFullScreen=function(e){return&quot;undefined&quot;==typeof e&amp;&amp;(e=t.body),&quot;&quot;===this.prefix?e.requestFullScreen():e[this.prefix+(&quot;ms&quot;==this.prefix?&quot;RequestFullscreen&quot;:&quot;RequestFullScreen&quot;)]()},e.cancelFullScreen=function(){return&quot;&quot;===this.prefix?t.cancelFullScreen():t[this.prefix+(&quot;ms&quot;==this.prefix?&quot;ExitFullscreen&quot;:&quot;CancelFullScreen&quot;)]()},e.element=function(){return&quot;&quot;===this.prefix?t.fullscreenElement:t[this.prefix+&quot;FullscreenElement&quot;]}),e}function E(){var t={supported:function(){if(!(&quot;localStorage&quot;in e))return!1;try{e.localStorage.setItem(&quot;___test&quot;,&quot;OK&quot;);var t=e.localStorage.getItem(&quot;___test&quot;);return e.localStorage.removeItem(&quot;___test&quot;),&quot;OK&quot;===t}catch(n){return!1}return!1}()};return t}function _(g,x){function _(t,n){x.debug&amp;&amp;e.console&amp;&amp;console[n?&quot;warn&quot;:&quot;log&quot;](t)}function F(){return{url:x.iconUrl,external:0===x.iconUrl.indexOf(&quot;http&quot;)}}function M(){var e=[],t=F(),n=(t.external?&quot;&quot;:t.url)+&quot;#&quot;+x.iconPrefix;return s(x.controls,&quot;play-large&quot;)&amp;&amp;e.push(&#39;&lt;button type=&quot;button&quot; data-plyr=&quot;play&quot; class=&quot;plyr__play-large&quot;&gt;&#39;,&#39;&lt;svg&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-play&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.play+&quot;&lt;/span&gt;&quot;,&quot;&lt;/button&gt;&quot;),e.push(&#39;&lt;div class=&quot;plyr__controls&quot;&gt;&#39;),s(x.controls,&quot;restart&quot;)&amp;&amp;e.push(&#39;&lt;button type=&quot;button&quot; data-plyr=&quot;restart&quot;&gt;&#39;,&#39;&lt;svg&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-restart&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.restart+&quot;&lt;/span&gt;&quot;,&quot;&lt;/button&gt;&quot;),s(x.controls,&quot;rewind&quot;)&amp;&amp;e.push(&#39;&lt;button type=&quot;button&quot; data-plyr=&quot;rewind&quot;&gt;&#39;,&#39;&lt;svg&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-rewind&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.rewind+&quot;&lt;/span&gt;&quot;,&quot;&lt;/button&gt;&quot;),s(x.controls,&quot;play&quot;)&amp;&amp;e.push(&#39;&lt;button type=&quot;button&quot; data-plyr=&quot;play&quot;&gt;&#39;,&#39;&lt;svg&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-play&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.play+&quot;&lt;/span&gt;&quot;,&quot;&lt;/button&gt;&quot;,&#39;&lt;button type=&quot;button&quot; data-plyr=&quot;pause&quot;&gt;&#39;,&#39;&lt;svg&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-pause&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.pause+&quot;&lt;/span&gt;&quot;,&quot;&lt;/button&gt;&quot;),s(x.controls,&quot;fast-forward&quot;)&amp;&amp;e.push(&#39;&lt;button type=&quot;button&quot; data-plyr=&quot;fast-forward&quot;&gt;&#39;,&#39;&lt;svg&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-fast-forward&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.forward+&quot;&lt;/span&gt;&quot;,&quot;&lt;/button&gt;&quot;),s(x.controls,&quot;progress&quot;)&amp;&amp;(e.push(&#39;&lt;span class=&quot;plyr__progress&quot;&gt;&#39;,&#39;&lt;label for=&quot;seek{id}&quot; class=&quot;plyr__sr-only&quot;&gt;Seek&lt;/label&gt;&#39;,&#39;&lt;input id=&quot;seek{id}&quot; class=&quot;plyr__progress--seek&quot; type=&quot;range&quot; min=&quot;0&quot; max=&quot;100&quot; step=&quot;0.1&quot; value=&quot;0&quot; data-plyr=&quot;seek&quot;&gt;&#39;,&#39;&lt;progress class=&quot;plyr__progress--played&quot; max=&quot;100&quot; value=&quot;0&quot; role=&quot;presentation&quot;&gt;&lt;/progress&gt;&#39;,&#39;&lt;progress class=&quot;plyr__progress--buffer&quot; max=&quot;100&quot; value=&quot;0&quot;&gt;&#39;,&quot;&lt;span&gt;0&lt;/span&gt;% &quot;+x.i18n.buffered,&quot;&lt;/progress&gt;&quot;),x.tooltips.seek&amp;&amp;e.push(&#39;&lt;span class=&quot;plyr__tooltip&quot;&gt;00:00&lt;/span&gt;&#39;),e.push(&quot;&lt;/span&gt;&quot;)),s(x.controls,&quot;current-time&quot;)&amp;&amp;e.push(&#39;&lt;span class=&quot;plyr__time&quot;&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.currentTime+&quot;&lt;/span&gt;&quot;,&#39;&lt;span class=&quot;plyr__time--current&quot;&gt;00:00&lt;/span&gt;&#39;,&quot;&lt;/span&gt;&quot;),s(x.controls,&quot;duration&quot;)&amp;&amp;e.push(&#39;&lt;span class=&quot;plyr__time&quot;&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.duration+&quot;&lt;/span&gt;&quot;,&#39;&lt;span class=&quot;plyr__time--duration&quot;&gt;00:00&lt;/span&gt;&#39;,&quot;&lt;/span&gt;&quot;),s(x.controls,&quot;mute&quot;)&amp;&amp;e.push(&#39;&lt;button type=&quot;button&quot; data-plyr=&quot;mute&quot;&gt;&#39;,&#39;&lt;svg class=&quot;icon--muted&quot;&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-muted&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;svg&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-volume&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.toggleMute+&quot;&lt;/span&gt;&quot;,&quot;&lt;/button&gt;&quot;),s(x.controls,&quot;volume&quot;)&amp;&amp;e.push(&#39;&lt;span class=&quot;plyr__volume&quot;&gt;&#39;,&#39;&lt;label for=&quot;volume{id}&quot; class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.volume+&quot;&lt;/label&gt;&quot;,&#39;&lt;input id=&quot;volume{id}&quot; class=&quot;plyr__volume--input&quot; type=&quot;range&quot; min=&quot;&#39;+x.volumeMin+&#39;&quot; max=&quot;&#39;+x.volumeMax+&#39;&quot; value=&quot;&#39;+x.volume+&#39;&quot; data-plyr=&quot;volume&quot;&gt;&#39;,&#39;&lt;progress class=&quot;plyr__volume--display&quot; max=&quot;&#39;+x.volumeMax+&#39;&quot; value=&quot;&#39;+x.volumeMin+&#39;&quot; role=&quot;presentation&quot;&gt;&lt;/progress&gt;&#39;,&quot;&lt;/span&gt;&quot;),s(x.controls,&quot;captions&quot;)&amp;&amp;e.push(&#39;&lt;button type=&quot;button&quot; data-plyr=&quot;captions&quot;&gt;&#39;,&#39;&lt;svg class=&quot;icon--captions-on&quot;&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-captions-on&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;svg&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-captions-off&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.toggleCaptions+&quot;&lt;/span&gt;&quot;,&quot;&lt;/button&gt;&quot;),s(x.controls,&quot;fullscreen&quot;)&amp;&amp;e.push(&#39;&lt;button type=&quot;button&quot; data-plyr=&quot;fullscreen&quot;&gt;&#39;,&#39;&lt;svg class=&quot;icon--exit-fullscreen&quot;&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-exit-fullscreen&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;svg&gt;&lt;use xlink:href=&quot;&#39;+n+&#39;-enter-fullscreen&quot; /&gt;&lt;/svg&gt;&#39;,&#39;&lt;span class=&quot;plyr__sr-only&quot;&gt;&#39;+x.i18n.toggleFullscreen+&quot;&lt;/span&gt;&quot;,&quot;&lt;/button&gt;&quot;),e.push(&quot;&lt;/div&gt;&quot;),e.join(&quot;&quot;)}function P(){if(Be.supported.full&amp;&amp;(&quot;audio&quot;!=Be.type||x.fullscreen.allowAudio)&amp;&amp;x.fullscreen.enabled){var e=I.supportsFullScreen;e||x.fullscreen.fallback&amp;&amp;!G()?(_((e?&quot;Native&quot;:&quot;Fallback&quot;)+&quot; fullscreen enabled&quot;),m(Be.container,x.classes.fullscreen.enabled,!0)):_(&quot;Fullscreen not supported and fallback disabled&quot;),k(Be.buttons.fullscreen,!1),W()}}function R(){if(&quot;video&quot;===Be.type){V(x.selectors.captions)||Be.videoContainer.insertAdjacentHTML(&quot;afterbegin&quot;,&#39;&lt;div class=&quot;&#39;+A(x.selectors.captions)+&#39;&quot;&gt;&lt;/div&gt;&#39;),Be.usingTextTracks=!1,Be.media.textTracks&amp;&amp;(Be.usingTextTracks=!0);for(var e,t=&quot;&quot;,n=Be.media.childNodes,a=0;a&lt;n.length;a++)&quot;track&quot;===n[a].nodeName.toLowerCase()&amp;&amp;(e=n[a].kind,&quot;captions&quot;!==e&amp;&amp;&quot;subtitles&quot;!==e||(t=n[a].getAttribute(&quot;src&quot;)));if(Be.captionExists=!0,&quot;&quot;===t?(Be.captionExists=!1,_(&quot;No caption track found&quot;)):_(&quot;Caption track found; URI: &quot;+t),Be.captionExists){for(var r=Be.media.textTracks,s=0;s&lt;r.length;s++)r[s].mode=&quot;hidden&quot;;if(O(Be),(&quot;IE&quot;===Be.browser.name&amp;&amp;Be.browser.version&gt;=10||&quot;Firefox&quot;===Be.browser.name&amp;&amp;Be.browser.version&gt;=31)&amp;&amp;(_(&quot;Detected browser with known TextTrack issues - using manual fallback&quot;),Be.usingTextTracks=!1),Be.usingTextTracks){_(&quot;TextTracks supported&quot;);for(var o=0;o&lt;r.length;o++){var i=r[o];&quot;captions&quot;!==i.kind&amp;&amp;&quot;subtitles&quot;!==i.kind||y(i,&quot;cuechange&quot;,function(){this.activeCues[0]&amp;&amp;&quot;text&quot;in this.activeCues[0]?L(this.activeCues[0].getCueAsHTML()):L()})}}else if(_(&quot;TextTracks not supported so rendering captions manually&quot;),Be.currentCaption=&quot;&quot;,Be.captions=[],&quot;&quot;!==t){var l=new XMLHttpRequest;l.onreadystatechange=function(){if(4===l.readyState)if(200===l.status){var e,t=[],n=l.responseText;t=n.split(&quot;\n\n&quot;);for(var a=0;a&lt;t.length;a++){e=t[a],Be.captions[a]=[];var r=e.split(&quot;\n&quot;),s=0;-1===r[s].indexOf(&quot;:&quot;)&amp;&amp;(s=1),Be.captions[a]=[r[s],r[s+1]]}Be.captions.shift(),_(&quot;Successfully loaded the caption file via AJAX&quot;)}else _(&quot;There was a problem loading the caption file via AJAX&quot;,!0)},l.open(&quot;get&quot;,t,!0),l.send()}}else m(Be.container,x.classes.captions.enabled)}}function L(e){var n=V(x.selectors.captions),a=t.createElement(&quot;span&quot;);n.innerHTML=&quot;&quot;,&quot;undefined&quot;==typeof e&amp;&amp;(e=&quot;&quot;),&quot;string&quot;==typeof e?a.innerHTML=e.trim():a.appendChild(e),n.appendChild(a);n.offsetHeight}function B(e){function t(e,t){var n=[];n=e.split(&quot; --&gt; &quot;);for(var a=0;a&lt;n.length;a++)n[a]=n[a].replace(/(\d+:\d+:\d+\.\d+).*/,&quot;$1&quot;);return r(n[t])}function n(e){return t(e,0)}function a(e){return t(e,1)}function r(e){if(null===e||void 0===e)return 0;var t,n=[],a=[];return n=e.split(&quot;,&quot;),a=n[0].split(&quot;:&quot;),t=Math.floor(60*a[0]*60)+Math.floor(60*a[1])+Math.floor(a[2])}if(!Be.usingTextTracks&amp;&amp;&quot;video&quot;===Be.type&amp;&amp;Be.supported.full&amp;&amp;(Be.subcount=0,e=&quot;number&quot;==typeof e?e:Be.media.currentTime,Be.captions[Be.subcount])){for(;a(Be.captions[Be.subcount][0])&lt;e.toFixed(1);)if(Be.subcount++,Be.subcount&gt;Be.captions.length-1){Be.subcount=Be.captions.length-1;break}Be.media.currentTime.toFixed(1)&gt;=n(Be.captions[Be.subcount][0])&amp;&amp;Be.media.currentTime.toFixed(1)&lt;=a(Be.captions[Be.subcount][0])?(Be.currentCaption=Be.captions[Be.subcount][1],L(Be.currentCaption)):L()}}function O(){Be.buttons.captions&amp;&amp;(m(Be.container,x.classes.captions.enabled,!0),x.captions.defaultActive&amp;&amp;(m(Be.container,x.classes.captions.active,!0),k(Be.buttons.captions,!0)))}function H(e){return Be.container.querySelectorAll(e)}function V(e){return H(e)[0]}function G(){try{return e.self!==e.top}catch(t){return!0}}function W(){function e(e){9===e.which&amp;&amp;Be.isFullscreen&amp;&amp;(e.target!==a||e.shiftKey?e.target===n&amp;&amp;e.shiftKey&amp;&amp;(e.preventDefault(),a.focus()):(e.preventDefault(),n.focus()))}var t=H(&quot;input:not([disabled]), button:not([disabled])&quot;),n=t[0],a=t[t.length-1];y(Be.container,&quot;keydown&quot;,e)}function Y(e,t){if(&quot;string&quot;==typeof t)d(e,Be.media,{src:t});else if(t.constructor===Array)for(var n=t.length-1;n&gt;=0;n--)d(e,Be.media,t[n])}function q(){if(x.loadSprite){var e=F();e.external?(_(&quot;Loading external SVG sprite&quot;),C(e.url)):_(&quot;Sprite will be used inline&quot;)}var n=x.html;_(&quot;Injecting custom controls&quot;),n||(n=M()),n=o(n,&quot;{seektime}&quot;,x.seekTime),n=o(n,&quot;{id}&quot;,Math.floor(1e4*Math.random()));var a;if(null!==x.selectors.controls.container&amp;&amp;(a=x.selectors.controls.container,&quot;string&quot;==typeof selector&amp;&amp;(a=t.querySelector(a))),a instanceof HTMLElement||(a=Be.container),a.insertAdjacentHTML(&quot;beforeend&quot;,n),x.tooltips.controls)for(var r=H([x.selectors.controls.wrapper,&quot; &quot;,x.selectors.labels,&quot; .&quot;,x.classes.hidden].join(&quot;&quot;)),s=r.length-1;s&gt;=0;s--){var i=r[s];m(i,x.classes.hidden,!1),m(i,x.classes.tooltip,!0)}}function z(){try{return Be.controls=V(x.selectors.controls.wrapper),Be.buttons={},Be.buttons.seek=V(x.selectors.buttons.seek),Be.buttons.play=H(x.selectors.buttons.play),Be.buttons.pause=V(x.selectors.buttons.pause),Be.buttons.restart=V(x.selectors.buttons.restart),Be.buttons.rewind=V(x.selectors.buttons.rewind),Be.buttons.forward=V(x.selectors.buttons.forward),Be.buttons.fullscreen=V(x.selectors.buttons.fullscreen),Be.buttons.mute=V(x.selectors.buttons.mute),Be.buttons.captions=V(x.selectors.buttons.captions),Be.progress={},Be.progress.container=V(x.selectors.progress.container),Be.progress.buffer={},Be.progress.buffer.bar=V(x.selectors.progress.buffer),Be.progress.buffer.text=Be.progress.buffer.bar&amp;&amp;Be.progress.buffer.bar.getElementsByTagName(&quot;span&quot;)[0],Be.progress.played=V(x.selectors.progress.played),Be.progress.tooltip=Be.progress.container&amp;&amp;Be.progress.container.querySelector(&quot;.&quot;+x.classes.tooltip),Be.volume={},Be.volume.input=V(x.selectors.volume.input),Be.volume.display=V(x.selectors.volume.display),Be.duration=V(x.selectors.duration),Be.currentTime=V(x.selectors.currentTime),Be.seekTime=H(x.selectors.seekTime),!0}catch(e){return _(&quot;It looks like there is a problem with your controls html&quot;,!0),X(!0),!1}}function Q(){m(Be.container,x.selectors.container.replace(&quot;.&quot;,&quot;&quot;),Be.supported.full)}function X(e){e?Be.media.setAttribute(&quot;controls&quot;,&quot;&quot;):Be.media.removeAttribute(&quot;controls&quot;)}function j(e){var t=x.i18n.play;if(&quot;undefined&quot;!=typeof x.title&amp;&amp;x.title.length&amp;&amp;(t+=&quot;, &quot;+x.title),Be.supported.full&amp;&amp;Be.buttons.play)for(var n=Be.buttons.play.length-1;n&gt;=0;n--)Be.buttons.play[n].setAttribute(&quot;aria-label&quot;,t);e instanceof HTMLElement&amp;&amp;e.setAttribute(&quot;title&quot;,x.i18n.frameTitle.replace(&quot;{title}&quot;,x.title))}function D(){if(!Be.media)return _(&quot;No audio or video element found&quot;,!0),!1;if(Be.supported.full&amp;&amp;(m(Be.container,x.classes.type.replace(&quot;{0}&quot;,Be.type),!0),s(x.types.embed,Be.type)&amp;&amp;m(Be.container,x.classes.type.replace(&quot;{0}&quot;,&quot;video&quot;),!0),m(Be.container,x.classes.stopped,x.autoplay),m(Be.container,x.classes.isIos,Be.browser.ios),m(Be.container,x.classes.isTouch,Be.browser.touch),&quot;video&quot;===Be.type)){var e=t.createElement(&quot;div&quot;);e.setAttribute(&quot;class&quot;,x.classes.videoWrapper),i(Be.media,e),Be.videoContainer=e}s(x.types.embed,Be.type)&amp;&amp;(U(),Be.embedId=null)}function U(){for(var n=t.createElement(&quot;div&quot;),a=Be.embedId,s=Be.type+&quot;-&quot;+Math.floor(1e4*Math.random()),o=H(&#39;[id^=&quot;&#39;+Be.type+&#39;-&quot;]&#39;),i=o.length-1;i&gt;=0;i--)u(o[i]);if(m(Be.media,x.classes.videoWrapper,!0),m(Be.media,x.classes.embedWrapper,!0),&quot;youtube&quot;===Be.type)Be.media.appendChild(n),n.setAttribute(&quot;id&quot;,s),&quot;object&quot;==typeof YT?$(a,n):(r(x.urls.youtube.api),e.onYouTubeReadyCallbacks=e.onYouTubeReadyCallbacks||[],e.onYouTubeReadyCallbacks.push(function(){$(a,n)}),e.onYouTubeIframeAPIReady=function(){e.onYouTubeReadyCallbacks.forEach(function(e){e()})});else if(&quot;vimeo&quot;===Be.type){var l=t.createElement(&quot;iframe&quot;);l.loaded=!1,y(l,&quot;load&quot;,function(){l.loaded=!0}),p(l,{src:&quot;https://player.vimeo.com/video/&quot;+a+&quot;?player_id=&quot;+s+&quot;&amp;api=1&amp;badge=0&amp;byline=0&amp;portrait=0&amp;title=0&quot;,id:s,webkitallowfullscreen:&quot;&quot;,mozallowfullscreen:&quot;&quot;,allowfullscreen:&quot;&quot;,frameborder:0}),Be.supported.full?(n.appendChild(l),Be.media.appendChild(n)):Be.media.appendChild(l),&quot;$f&quot;in e||r(x.urls.vimeo.api);var c=e.setInterval(function(){&quot;$f&quot;in e&amp;&amp;l.loaded&amp;&amp;(e.clearInterval(c),J.call(l))},50)}else if(&quot;soundcloud&quot;===Be.type){var d=t.createElement(&quot;iframe&quot;);d.loaded=!1,y(d,&quot;load&quot;,function(){d.loaded=!0}),p(d,{src:&quot;https://w.soundcloud.com/player/?url=https://api.soundcloud.com/tracks/&quot;+a,id:s}),n.appendChild(d),Be.media.appendChild(n),e.SC||r(x.urls.soundcloud.api);var A=e.setInterval(function(){e.SC&amp;&amp;d.loaded&amp;&amp;(e.clearInterval(A),K.call(d))},50)}}function Z(){Be.container.plyr.embed=Be.embed,Le(),j(V(&quot;iframe&quot;))}function $(t,n){&quot;timer&quot;in Be||(Be.timer={}),Be.embed=new YT.Player(n.id,{videoId:t,playerVars:{autoplay:x.autoplay?1:0,controls:Be.supported.full?0:1,rel:0,showinfo:0,iv_load_policy:3,cc_load_policy:x.captions.defaultActive?1:0,cc_lang_pref:&quot;en&quot;,wmode:&quot;transparent&quot;,modestbranding:1,disablekb:1,origin:&quot;*&quot;},events:{onError:function(e){h(Be.container,&quot;error&quot;,!0,{code:e.data,embed:e.target})},onReady:function(t){var n=t.target;Be.media.play=function(){n.playVideo(),Be.media.paused=!1},Be.media.pause=function(){n.pauseVideo(),Be.media.paused=!0},Be.media.stop=function(){n.stopVideo(),Be.media.paused=!0},Be.media.duration=n.getDuration(),Be.media.paused=!0,Be.media.currentTime=n.getCurrentTime(),Be.media.muted=n.isMuted(),x.title=n.getVideoData().title,h(Be.media,&quot;timeupdate&quot;),e.clearInterval(Be.timer.buffering),Be.timer.buffering=e.setInterval(function(){Be.media.buffered=n.getVideoLoadedFraction(),h(Be.media,&quot;progress&quot;),1===Be.media.buffered&amp;&amp;(e.clearInterval(Be.timer.buffering),h(Be.media,&quot;canplaythrough&quot;))},200),Z(),we()},onStateChange:function(t){var n=t.target;switch(e.clearInterval(Be.timer.playing),t.data){case 0:Be.media.paused=!0,h(Be.media,&quot;ended&quot;);break;case 1:Be.media.paused=!1,Be.media.seeking=!1,h(Be.media,&quot;play&quot;),h(Be.media,&quot;playing&quot;),Be.timer.playing=e.setInterval(function(){Be.media.currentTime=n.getCurrentTime(),h(Be.media,&quot;timeupdate&quot;)},100);break;case 2:Be.media.paused=!0,h(Be.media,&quot;pause&quot;)}h(Be.container,&quot;statechange&quot;,!1,{code:t.data})}}})}function J(){Be.embed=$f(this),Be.embed.addEvent(&quot;ready&quot;,function(){Be.media.play=function(){Be.embed.api(&quot;play&quot;),Be.media.paused=!1},Be.media.pause=function(){Be.embed.api(&quot;pause&quot;),Be.media.paused=!0},Be.media.stop=function(){Be.embed.api(&quot;stop&quot;),Be.media.paused=!0},Be.media.paused=!0,Be.media.currentTime=0,Z(),Be.embed.api(&quot;getCurrentTime&quot;,function(e){Be.media.currentTime=e,h(Be.media,&quot;timeupdate&quot;)}),Be.embed.api(&quot;getDuration&quot;,function(e){Be.media.duration=e,we()}),Be.embed.addEvent(&quot;play&quot;,function(){Be.media.paused=!1,h(Be.media,&quot;play&quot;),h(Be.media,&quot;playing&quot;)}),Be.embed.addEvent(&quot;pause&quot;,function(){Be.media.paused=!0,h(Be.media,&quot;pause&quot;)}),Be.embed.addEvent(&quot;playProgress&quot;,function(e){Be.media.seeking=!1,Be.media.currentTime=e.seconds,h(Be.media,&quot;timeupdate&quot;)}),Be.embed.addEvent(&quot;loadProgress&quot;,function(e){Be.media.buffered=e.percent,h(Be.media,&quot;progress&quot;),1===parseInt(e.percent)&amp;&amp;h(Be.media,&quot;canplaythrough&quot;)}),Be.embed.addEvent(&quot;finish&quot;,function(){Be.media.paused=!0,h(Be.media,&quot;ended&quot;)}),x.autoplay&amp;&amp;Be.embed.api(&quot;play&quot;)})}function K(){Be.embed=e.SC.Widget(this),Be.embed.bind(e.SC.Widget.Events.READY,function(){Be.media.play=function(){Be.embed.play(),Be.media.paused=!1},Be.media.pause=function(){Be.embed.pause(),Be.media.paused=!0},Be.media.stop=function(){Be.embed.seekTo(0),Be.embed.pause(),Be.media.paused=!0},Be.media.paused=!0,Be.media.currentTime=0,Z(),Be.embed.getPosition(function(e){Be.media.currentTime=e,h(Be.media,&quot;timeupdate&quot;)}),Be.embed.getDuration(function(e){Be.media.duration=e/1e3,we()}),Be.embed.bind(e.SC.Widget.Events.PLAY,function(){Be.media.paused=!1,h(Be.media,&quot;play&quot;),h(Be.media,&quot;playing&quot;)}),Be.embed.bind(e.SC.Widget.Events.PAUSE,function(){Be.media.paused=!0,h(Be.media,&quot;pause&quot;)}),Be.embed.bind(e.SC.Widget.Events.PLAY_PROGRESS,function(e){Be.media.seeking=!1,Be.media.currentTime=e.currentPosition/1e3,h(Be.media,&quot;timeupdate&quot;)}),Be.embed.bind(e.SC.Widget.Events.LOAD_PROGRESS,function(e){Be.media.buffered=e.loadProgress,h(Be.media,&quot;progress&quot;),1===parseInt(e.loadProgress)&amp;&amp;h(Be.media,&quot;canplaythrough&quot;)}),Be.embed.bind(e.SC.Widget.Events.FINISH,function(){Be.media.paused=!0,h(Be.media,&quot;ended&quot;)}),x.autoplay&amp;&amp;Be.embed.play()})}function ee(){&quot;play&quot;in Be.media&amp;&amp;Be.media.play()}function te(){&quot;pause&quot;in Be.media&amp;&amp;Be.media.pause()}function ne(e){e===!0?ee():e===!1?te():Be.media[Be.media.paused?&quot;play&quot;:&quot;pause&quot;]()}function ae(e){&quot;number&quot;!=typeof e&amp;&amp;(e=x.seekTime),se(Be.media.currentTime-e)}function re(e){&quot;number&quot;!=typeof e&amp;&amp;(e=x.seekTime),se(Be.media.currentTime+e)}function se(e){var t=0,n=Be.media.paused,a=oe();&quot;number&quot;==typeof e?t=e:&quot;object&quot;!=typeof e||&quot;input&quot;!==e.type&amp;&amp;&quot;change&quot;!==e.type||(t=e.target.value/e.target.max*a),0&gt;t?t=0:t&gt;a&amp;&amp;(t=a),Te(t);try{Be.media.currentTime=t.toFixed(1)}catch(r){}if(s(x.types.embed,Be.type)){switch(Be.type){case&quot;youtube&quot;:Be.embed.seekTo(t);break;case&quot;vimeo&quot;:Be.embed.api(&quot;seekTo&quot;,t.toFixed(0));break;case&quot;soundcloud&quot;:Be.embed.seekTo(1e3*t)}n&amp;&amp;te(),h(Be.media,&quot;timeupdate&quot;),Be.media.seeking=!0}_(&quot;Seeking to &quot;+Be.media.currentTime+&quot; seconds&quot;),B(t)}function oe(){var e=parseInt(x.duration),t=0;return null===Be.media.duration||isNaN(Be.media.duration)||(t=Be.media.duration),isNaN(e)?t:e}function ie(){m(Be.container,x.classes.playing,!Be.media.paused),m(Be.container,x.classes.stopped,Be.media.paused),_e(Be.media.paused)}function le(){N={x:e.pageXOffset||0,y:e.pageYOffset||0}}function ue(){e.scrollTo(N.x,N.y)}function ce(e){var n=I.supportsFullScreen;e&amp;&amp;e.type===I.fullScreenEventName?Be.isFullscreen=I.isFullScreen(Be.container):n?(I.isFullScreen(Be.container)?I.cancelFullScreen():(le(),I.requestFullScreen(Be.container)),Be.isFullscreen=I.isFullScreen(Be.container)):(Be.isFullscreen=!Be.isFullscreen,Be.isFullscreen?(y(t,&quot;keyup&quot;,pe),t.body.style.overflow=&quot;hidden&quot;):(b(t,&quot;keyup&quot;,pe),t.body.style.overflow=&quot;&quot;)),m(Be.container,x.classes.fullscreen.active,Be.isFullscreen),Be.isFullscreen?Be.container.setAttribute(&quot;tabindex&quot;,&quot;-1&quot;):Be.container.removeAttribute(&quot;tabindex&quot;),W(Be.isFullscreen),k(Be.buttons.fullscreen,Be.isFullscreen),h(Be.container,Be.isFullscreen?&quot;enterfullscreen&quot;:&quot;exitfullscreen&quot;),!Be.isFullscreen&amp;&amp;n&amp;&amp;ue()}function pe(e){27===(e.which||e.charCode||e.keyCode)&amp;&amp;Be.isFullscreen&amp;&amp;ce()}function de(e){if(&quot;boolean&quot;!=typeof e&amp;&amp;(e=!Be.media.muted),k(Be.buttons.mute,e),Be.media.muted=e,0===Be.media.volume&amp;&amp;Ae(x.volume),s(x.types.embed,Be.type)){switch(Be.type){case&quot;youtube&quot;:Be.embed[Be.media.muted?&quot;mute&quot;:&quot;unMute&quot;]();break;case&quot;vimeo&quot;:Be.embed.api(&quot;setVolume&quot;,Be.media.muted?0:parseFloat(x.volume/x.volumeMax));break;case&quot;soundcloud&quot;:Be.embed.setVolume(Be.media.muted?0:parseFloat(x.volume/x.volumeMax))}h(Be.media,&quot;volumechange&quot;)}}function Ae(t){var n=x.volumeMax,a=x.volumeMin;if(&quot;undefined&quot;==typeof t&amp;&amp;(t=x.volume,x.storage.enabled&amp;&amp;E().supported&amp;&amp;(t=e.localStorage.getItem(x.storage.key),e.localStorage.removeItem(&quot;plyr-volume&quot;))),(null===t||isNaN(t))&amp;&amp;(t=x.volume),t&gt;n&amp;&amp;(t=n),a&gt;t&amp;&amp;(t=a),Be.media.volume=parseFloat(t/n),Be.volume.display&amp;&amp;(Be.volume.display.value=t),s(x.types.embed,Be.type)){switch(Be.type){case&quot;youtube&quot;:Be.embed.setVolume(100*Be.media.volume);break;case&quot;vimeo&quot;:Be.embed.api(&quot;setVolume&quot;,Be.media.volume);break;case&quot;soundcloud&quot;:Be.embed.setVolume(Be.media.volume)}h(Be.media,&quot;volumechange&quot;)}Be.media.muted&amp;&amp;t&gt;0&amp;&amp;de()}function me(){var e=Be.media.muted?0:Be.media.volume*x.volumeMax;Ae(e+x.volumeStep/5)}function fe(){var e=Be.media.muted?0:Be.media.volume*x.volumeMax;Ae(e-x.volumeStep/5)}function ye(){var t=Be.media.muted?0:Be.media.volume*x.volumeMax;Be.supported.full&amp;&amp;(Be.volume.input&amp;&amp;(Be.volume.input.value=t),Be.volume.display&amp;&amp;(Be.volume.display.value=t)),x.storage.enabled&amp;&amp;E().supported&amp;&amp;!isNaN(t)&amp;&amp;e.localStorage.setItem(x.storage.key,t),m(Be.container,x.classes.muted,0===t),Be.supported.full&amp;&amp;Be.buttons.mute&amp;&amp;k(Be.buttons.mute,0===t)}function be(e){Be.supported.full&amp;&amp;Be.buttons.captions&amp;&amp;(&quot;boolean&quot;!=typeof e&amp;&amp;(e=-1===Be.container.className.indexOf(x.classes.captions.active)),Be.captionsEnabled=e,k(Be.buttons.captions,Be.captionsEnabled),m(Be.container,x.classes.captions.active,Be.captionsEnabled),h(Be.container,Be.captionsEnabled?&quot;captionsenabled&quot;:&quot;captionsdisabled&quot;))}function ve(e){var t=&quot;waiting&quot;===e.type;clearTimeout(Be.timers.loading),Be.timers.loading=setTimeout(function(){m(Be.container,x.classes.loading,t)},t?250:0)}function ge(e){if(Be.supported.full){var t=Be.progress.played,n=0,a=oe();if(e)switch(e.type){case&quot;timeupdate&quot;:case&quot;seeking&quot;:n=w(Be.media.currentTime,a),&quot;timeupdate&quot;==e.type&amp;&amp;Be.buttons.seek&amp;&amp;(Be.buttons.seek.value=n);break;case&quot;playing&quot;:case&quot;progress&quot;:t=Be.progress.buffer,n=function(){var e=Be.media.buffered;return e&amp;&amp;e.length?w(e.end(0),a):&quot;number&quot;==typeof e?100*e:0}()}he(t,n)}}function he(e,t){if(Be.supported.full){if(&quot;undefined&quot;==typeof t&amp;&amp;(t=0),&quot;undefined&quot;==typeof e){if(!Be.progress||!Be.progress.buffer)return;e=Be.progress.buffer}e instanceof HTMLElement?e.value=t:e&amp;&amp;(e.bar&amp;&amp;(e.bar.value=t),e.text&amp;&amp;(e.text.innerHTML=t))}}function ke(e,t){if(t){isNaN(e)&amp;&amp;(e=0),Be.secs=parseInt(e%60),Be.mins=parseInt(e/60%60),Be.hours=parseInt(e/60/60%60);var n=parseInt(oe()/60/60%60)&gt;0;Be.secs=(&quot;0&quot;+Be.secs).slice(-2),Be.mins=(&quot;0&quot;+Be.mins).slice(-2),t.innerHTML=(n?Be.hours+&quot;:&quot;:&quot;&quot;)+Be.mins+&quot;:&quot;+Be.secs}}function we(){if(Be.supported.full){var e=oe()||0;!Be.duration&amp;&amp;x.displayDuration&amp;&amp;Be.media.paused&amp;&amp;ke(e,Be.currentTime),Be.duration&amp;&amp;ke(e,Be.duration),Ee()}}function xe(e){ke(Be.media.currentTime,Be.currentTime),e&amp;&amp;&quot;timeupdate&quot;==e.type&amp;&amp;Be.media.seeking||ge(e)}function Te(e){&quot;number&quot;!=typeof e&amp;&amp;(e=0);var t=oe(),n=w(e,t);Be.progress&amp;&amp;Be.progress.played&amp;&amp;(Be.progress.played.value=n),Be.buttons&amp;&amp;Be.buttons.seek&amp;&amp;(Be.buttons.seek.value=n)}function Ee(e){var t=oe();if(x.tooltips.seek&amp;&amp;Be.progress.container&amp;&amp;0!==t){var n=Be.progress.container.getBoundingClientRect(),a=0,r=x.classes.tooltip+&quot;--visible&quot;;if(e)a=100/n.width*(e.pageX-n.left);else{if(!f(Be.progress.tooltip,r))return;a=Be.progress.tooltip.style.left.replace(&quot;%&quot;,&quot;&quot;)}0&gt;a?a=0:a&gt;100&amp;&amp;(a=100),ke(t/100*a,Be.progress.tooltip),Be.progress.tooltip.style.left=a+&quot;%&quot;,e&amp;&amp;s([&quot;mouseenter&quot;,&quot;mouseleave&quot;],e.type)&amp;&amp;m(Be.progress.tooltip,r,&quot;mouseenter&quot;===e.type)}}function _e(t){if(x.hideControls&amp;&amp;&quot;audio&quot;!==Be.type){var n=0,a=!1,r=t;if(&quot;boolean&quot;!=typeof t&amp;&amp;(t&amp;&amp;t.type?(a=&quot;enterfullscreen&quot;===t.type,r=s([&quot;mousemove&quot;,&quot;mouseenter&quot;,&quot;focus&quot;],t.type),&quot;mousemove&quot;===t.type&amp;&amp;(n=2e3),&quot;focus&quot;===t.type&amp;&amp;(n=3e3)):r=!f(Be.container,x.classes.hideControls)),e.clearTimeout(Be.timers.hover),r||Be.media.paused){if(m(Be.container,x.classes.hideControls,!1),Be.media.paused)return;Be.browser.touch&amp;&amp;(n=3e3)}r&amp;&amp;Be.media.paused||(Be.timers.hover=e.setTimeout(function(){Be.controls.active&amp;&amp;!a||m(Be.container,x.classes.hideControls,!0)},n))}}function Ce(e){if(&quot;undefined&quot;!=typeof e)return void Se(e);var t;switch(Be.type){case&quot;youtube&quot;:t=Be.embed.getVideoUrl();break;case&quot;vimeo&quot;:Be.embed.api(&quot;getVideoUrl&quot;,function(e){t=e});break;case&quot;soundcloud&quot;:Be.embed.getCurrentSound(function(e){t=e.permalink_url});break;default:t=Be.media.currentSrc}return t||&quot;&quot;}function Se(n){if(!(&quot;undefined&quot;!=typeof n&amp;&amp;&quot;sources&quot;in n&amp;&amp;n.sources.length))return void _(&quot;Invalid source format&quot;,!0);if(te(),Te(),he(),Me(),&quot;youtube&quot;===Be.type?(Be.embed.destroy(),e.clearInterval(Be.timer.buffering),e.clearInterval(Be.timer.playing)):&quot;video&quot;===Be.type&amp;&amp;Be.videoContainer&amp;&amp;u(Be.videoContainer),Be.embed=null,u(Be.media),&quot;type&quot;in n&amp;&amp;(Be.type=n.type,&quot;video&quot;===Be.type)){var a=n.sources[0];&quot;type&quot;in a&amp;&amp;s(x.types.embed,a.type)&amp;&amp;(Be.type=a.type)}switch(Be.supported=S(Be.type),Be.type){case&quot;video&quot;:Be.media=t.createElement(&quot;video&quot;);break;case&quot;audio&quot;:Be.media=t.createElement(&quot;audio&quot;);break;case&quot;youtube&quot;:case&quot;vimeo&quot;:case&quot;soundcloud&quot;:Be.media=t.createElement(&quot;div&quot;),Be.embedId=n.sources[0].src}c(Be.container,Be.media),&quot;undefined&quot;!=typeof n.autoplay&amp;&amp;(x.autoplay=n.autoplay),s(x.types.html5,Be.type)&amp;&amp;(x.crossorigin&amp;&amp;Be.media.setAttribute(&quot;crossorigin&quot;,&quot;&quot;),x.autoplay&amp;&amp;Be.media.setAttribute(&quot;autoplay&quot;,&quot;&quot;),&quot;poster&quot;in n&amp;&amp;Be.media.setAttribute(&quot;poster&quot;,n.poster),x.loop&amp;&amp;Be.media.setAttribute(&quot;loop&quot;,&quot;&quot;)),Be.container.className=Be.originalClassName,m(Be.container,x.classes.fullscreen.active,Be.isFullscreen),m(Be.container,x.classes.captions.active,Be.captionsEnabled),Q(),s(x.types.html5,Be.type)&amp;&amp;Y(&quot;source&quot;,n.sources),D(),s(x.types.html5,Be.type)&amp;&amp;(&quot;tracks&quot;in n&amp;&amp;Y(&quot;track&quot;,n.tracks),Be.media.load(),Le(),we()),x.title=n.title,j(),Be.container.plyr.media=Be.media}function Fe(e){&quot;video&quot;===Be.type&amp;&amp;Be.media.setAttribute(&quot;poster&quot;,e)}function Ie(){function n(){var e=Be.media.paused;e?ee():te();var t=Be.buttons[e?&quot;play&quot;:&quot;pause&quot;],n=Be.buttons[e?&quot;pause&quot;:&quot;play&quot;];if(n=n&amp;&amp;n.length&gt;1?n[n.length-1]:n[0]){var a=f(t,x.classes.tabFocus);setTimeout(function(){n.focus(),a&amp;&amp;(m(t,x.classes.tabFocus,!1),m(n,x.classes.tabFocus,!0))},100)}}function a(){var e=t.activeElement;e&amp;&amp;e!=t.body?t.querySelector&amp;&amp;(e=t.querySelector(&quot;:focus&quot;)):e=null;for(var n in Be.buttons){var a=Be.buttons[n];if(a instanceof NodeList)for(var r=0;r&lt;a.length;r++)m(a[r],x.classes.tabFocus,a[r]===e);else m(a,x.classes.tabFocus,a===e)}}var r=&quot;IE&quot;==Be.browser.name?&quot;change&quot;:&quot;input&quot;;y(e,&quot;keyup&quot;,function(e){var t=e.keyCode?e.keyCode:e.which;9==t&amp;&amp;a()}),y(t.body,&quot;click&quot;,function(){m(V(&quot;.&quot;+x.classes.tabFocus),x.classes.tabFocus,!1)});for(var s in Be.buttons){var o=Be.buttons[s];y(o,&quot;blur&quot;,function(){m(o,&quot;tab-focus&quot;,!1)})}v(Be.buttons.play,&quot;click&quot;,x.listeners.play,n),v(Be.buttons.pause,&quot;click&quot;,x.listeners.pause,n),v(Be.buttons.restart,&quot;click&quot;,x.listeners.restart,se),v(Be.buttons.rewind,&quot;click&quot;,x.listeners.rewind,ae),v(Be.buttons.forward,&quot;click&quot;,x.listeners.forward,re),v(Be.buttons.seek,r,x.listeners.seek,se),v(Be.volume.input,r,x.listeners.volume,function(){Ae(Be.volume.input.value)}),v(Be.buttons.mute,&quot;click&quot;,x.listeners.mute,de),v(Be.buttons.fullscreen,&quot;click&quot;,x.listeners.fullscreen,ce),I.supportsFullScreen&amp;&amp;y(t,I.fullScreenEventName,ce),y(Be.buttons.captions,&quot;click&quot;,be),y(Be.progress.container,&quot;mouseenter mouseleave mousemove&quot;,Ee),x.hideControls&amp;&amp;(y(Be.container,&quot;mouseenter mouseleave mousemove enterfullscreen&quot;,_e),y(Be.controls,&quot;mouseenter mouseleave&quot;,function(e){Be.controls.active=&quot;mouseenter&quot;===e.type}),y(Be.controls,&quot;focus blur&quot;,_e,!0)),y(Be.volume.input,&quot;wheel&quot;,function(e){e.preventDefault(),(e.deltaY&lt;0||e.deltaX&gt;0)&amp;&amp;fe(),(e.deltaY&gt;0||e.deltaX&lt;0)&amp;&amp;me()})}function Ne(){if(y(Be.media,&quot;timeupdate seeking&quot;,xe),y(Be.media,&quot;timeupdate&quot;,B),y(Be.media,&quot;durationchange loadedmetadata&quot;,we),y(Be.media,&quot;ended&quot;,function(){&quot;video&quot;===Be.type&amp;&amp;L(),ie(),se(0),we(),&quot;video&quot;===Be.type&amp;&amp;x.showPosterOnEnd&amp;&amp;Be.media.load()}),y(Be.media,&quot;progress playing&quot;,ge),y(Be.media,&quot;volumechange&quot;,ye),y(Be.media,&quot;play pause&quot;,ie),y(Be.media,&quot;waiting canplay seeked&quot;,ve),x.clickToPlay&amp;&amp;&quot;audio&quot;!==Be.type){var e=V(&quot;.&quot;+x.classes.videoWrapper);if(!e)return;e.style.cursor=&quot;pointer&quot;,y(e,&quot;click&quot;,function(){return Be.browser.touch&amp;&amp;!Be.media.paused?void _e(!0):void(Be.media.paused?ee():Be.media.ended?(se(),ee()):te())})}y(Be.media,x.events.join(&quot; &quot;),function(e){h(Be.container,e.type,!0);</td>
      </tr>
      <tr>
        <td id="L2" class="blob-num js-line-number" data-line-number="2"></td>
        <td id="LC2" class="blob-code blob-code-inner js-file-line">})}function Me(){if(s(x.types.html5,Be.type)){for(var e=Be.media.querySelectorAll(&quot;source&quot;),t=0;t&lt;e.length;t++)u(e[t]);Be.media.setAttribute(&quot;src&quot;,&quot;data:video/mp4;base64,AAAAHGZ0eXBpc29tAAACAGlzb21pc28ybXA0MQAAAAhmcmVlAAAAGm1kYXQAAAGzABAHAAABthBgUYI9t+8AAAMNbW9vdgAAAGxtdmhkAAAAAMXMvvrFzL76AAAD6AAAACoAAQAAAQAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAABhpb2RzAAAAABCAgIAHAE/////+/wAAAiF0cmFrAAAAXHRraGQAAAAPxcy++sXMvvoAAAABAAAAAAAAACoAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAAgAAAAIAAAAAAG9bWRpYQAAACBtZGhkAAAAAMXMvvrFzL76AAAAGAAAAAEVxwAAAAAALWhkbHIAAAAAAAAAAHZpZGUAAAAAAAAAAAAAAABWaWRlb0hhbmRsZXIAAAABaG1pbmYAAAAUdm1oZAAAAAEAAAAAAAAAAAAAACRkaW5mAAAAHGRyZWYAAAAAAAAAAQAAAAx1cmwgAAAAAQAAAShzdGJsAAAAxHN0c2QAAAAAAAAAAQAAALRtcDR2AAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAgACABIAAAASAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGP//AAAAXmVzZHMAAAAAA4CAgE0AAQAEgICAPyARAAAAAAMNQAAAAAAFgICALQAAAbABAAABtYkTAAABAAAAASAAxI2IAMUARAEUQwAAAbJMYXZjNTMuMzUuMAaAgIABAgAAABhzdHRzAAAAAAAAAAEAAAABAAAAAQAAABxzdHNjAAAAAAAAAAEAAAABAAAAAQAAAAEAAAAUc3RzegAAAAAAAAASAAAAAQAAABRzdGNvAAAAAAAAAAEAAAAsAAAAYHVkdGEAAABYbWV0YQAAAAAAAAAhaGRscgAAAAAAAAAAbWRpcmFwcGwAAAAAAAAAAAAAAAAraWxzdAAAACOpdG9vAAAAG2RhdGEAAAABAAAAAExhdmY1My4yMS4x&quot;),Be.media.load(),_(&quot;Cancelled network requests for old media&quot;)}}function Pe(){if(!Be.init)return null;if(Be.container.setAttribute(&quot;class&quot;,A(x.selectors.container)),Be.init=!1,u(V(x.selectors.controls.wrapper)),&quot;youtube&quot;===Be.type)return void Be.embed.destroy();&quot;video&quot;===Be.type&amp;&amp;(u(V(x.selectors.captions)),l(Be.videoContainer)),X(!0);var e=Be.media.cloneNode(!0);Be.media.parentNode.replaceChild(e,Be.media)}function Re(){if(Be.init)return null;if(I=T(),Be.browser=n(),Be.media=Be.container.querySelectorAll(&quot;audio, video&quot;)[0],Be.media||(Be.media=Be.container.querySelectorAll(&quot;div&quot;)[0]),Be.media){Be.originalClassName=Be.container.className;var e=Be.media.tagName.toLowerCase();if(&quot;div&quot;===e?(Be.type=Be.media.getAttribute(&quot;data-type&quot;),Be.embedId=Be.media.getAttribute(&quot;data-video-id&quot;),Be.media.removeAttribute(&quot;data-type&quot;),Be.media.removeAttribute(&quot;data-video-id&quot;)):(Be.type=e,x.crossorigin=null!==Be.media.getAttribute(&quot;crossorigin&quot;),x.autoplay=x.autoplay||null!==Be.media.getAttribute(&quot;autoplay&quot;),x.loop=x.loop||null!==Be.media.getAttribute(&quot;loop&quot;)),Be.supported=S(Be.type),Q(),!Be.supported.basic)return!1;if(_(Be.browser.name+&quot; &quot;+Be.browser.version),D(),s(x.types.html5,Be.type)){if(!Be.supported.full)return void(Be.init=!0);Le(),j(),x.autoplay&amp;&amp;ee()}Be.init=!0}}function Le(){if(!Be.supported.full)return _(&quot;No full support for this media type (&quot;+Be.type+&quot;)&quot;,!0),u(V(x.selectors.controls.wrapper)),u(V(x.selectors.buttons.play)),void X(!0);var e=!H(x.selectors.controls.wrapper).length;e&amp;&amp;q(),z()&amp;&amp;(e&amp;&amp;Ie(),Ne(),X(),P(),R(),Ae(),ye(),xe(),ie(),we(),h(Be.container,&quot;ready&quot;))}var Be=this;return Be.container=g,Be.timers={},_(x),Re(),Be.init?{media:Be.media,play:ee,pause:te,restart:se,rewind:ae,forward:re,seek:se,source:Ce,poster:Fe,setVolume:Ae,togglePlay:ne,toggleMute:de,toggleCaptions:be,toggleFullscreen:ce,toggleControls:_e,isFullscreen:function(){return Be.isFullscreen||!1},support:function(e){return a(Be,e)},destroy:Pe,restore:Re}:{}}function C(e){var n=new XMLHttpRequest;&quot;withCredentials&quot;in n&amp;&amp;(n.open(&quot;GET&quot;,e,!0),n.onload=function(){var e=t.createElement(&quot;div&quot;);e.setAttribute(&quot;hidden&quot;,&quot;&quot;),e.innerHTML=n.responseText,t.body.insertBefore(e,t.body.childNodes[0])},n.send())}function S(e){var a,r,s=n(),o=&quot;IE&quot;===s.name&amp;&amp;s.version&lt;=9,i=/iPhone|iPod/i.test(navigator.userAgent),l=!!t.createElement(&quot;audio&quot;).canPlayType,u=!!t.createElement(&quot;video&quot;).canPlayType;switch(e){case&quot;video&quot;:a=u,r=a&amp;&amp;!o&amp;&amp;!i;break;case&quot;audio&quot;:a=l,r=a&amp;&amp;!o;break;case&quot;vimeo&quot;:case&quot;youtube&quot;:case&quot;soundcloud&quot;:a=!0,r=!o&amp;&amp;!i;break;default:a=l&amp;&amp;u,r=a&amp;&amp;!o}return{basic:a,full:r}}function F(e,n){var a=[];if(&quot;string&quot;==typeof e?e=t.querySelectorAll(e):e instanceof HTMLElement?e=[e]:e instanceof NodeList||&quot;string&quot;==typeof e||(&quot;undefined&quot;==typeof n&amp;&amp;&quot;object&quot;==typeof e&amp;&amp;(n=e),e=t.querySelectorAll(M.selectors.container)),!S().basic||!e.length)return!1;for(var r=0;r&lt;e.length;r++){var s=e[r];if(&quot;undefined&quot;==typeof s.plyr){var o=x(M,n,JSON.parse(s.getAttribute(&quot;data-plyr&quot;)));if(!o.enabled)return;var i=new _(s,o);s.plyr=Object.keys(i).length?i:!1,h(s,&quot;setup&quot;,{plyr:s.plyr})}a.push(s.plyr)}return a}var I,N={x:0,y:0},M={enabled:!0,debug:!1,autoplay:!1,loop:!1,seekTime:10,volume:5,volumeMin:0,volumeMax:10,volumeStep:1,duration:null,displayDuration:!0,loadSprite:!0,iconPrefix:&quot;plyr&quot;,iconUrl:&quot;https://cdn.plyr.io/1.6.15/plyr.svg&quot;,clickToPlay:!0,hideControls:!0,showPosterOnEnd:!1,tooltips:{controls:!1,seek:!0},selectors:{container:&quot;.plyr&quot;,controls:{container:null,wrapper:&quot;.plyr__controls&quot;},labels:&quot;[data-plyr]&quot;,buttons:{seek:&#39;[data-plyr=&quot;seek&quot;]&#39;,play:&#39;[data-plyr=&quot;play&quot;]&#39;,pause:&#39;[data-plyr=&quot;pause&quot;]&#39;,restart:&#39;[data-plyr=&quot;restart&quot;]&#39;,rewind:&#39;[data-plyr=&quot;rewind&quot;]&#39;,forward:&#39;[data-plyr=&quot;fast-forward&quot;]&#39;,mute:&#39;[data-plyr=&quot;mute&quot;]&#39;,captions:&#39;[data-plyr=&quot;captions&quot;]&#39;,fullscreen:&#39;[data-plyr=&quot;fullscreen&quot;]&#39;},volume:{input:&#39;[data-plyr=&quot;volume&quot;]&#39;,display:&quot;.plyr__volume--display&quot;},progress:{container:&quot;.plyr__progress&quot;,buffer:&quot;.plyr__progress--buffer&quot;,played:&quot;.plyr__progress--played&quot;},captions:&quot;.plyr__captions&quot;,currentTime:&quot;.plyr__time--current&quot;,duration:&quot;.plyr__time--duration&quot;},classes:{videoWrapper:&quot;plyr__video-wrapper&quot;,embedWrapper:&quot;plyr__video-embed&quot;,type:&quot;plyr--{0}&quot;,stopped:&quot;plyr--stopped&quot;,playing:&quot;plyr--playing&quot;,muted:&quot;plyr--muted&quot;,loading:&quot;plyr--loading&quot;,hover:&quot;plyr--hover&quot;,tooltip:&quot;plyr__tooltip&quot;,hidden:&quot;plyr__sr-only&quot;,hideControls:&quot;plyr--hide-controls&quot;,isIos:&quot;plyr--is-ios&quot;,isTouch:&quot;plyr--is-touch&quot;,captions:{enabled:&quot;plyr--captions-enabled&quot;,active:&quot;plyr--captions-active&quot;},fullscreen:{enabled:&quot;plyr--fullscreen-enabled&quot;,active:&quot;plyr--fullscreen-active&quot;},tabFocus:&quot;tab-focus&quot;},captions:{defaultActive:!1},fullscreen:{enabled:!0,fallback:!0,allowAudio:!1},storage:{enabled:!0,key:&quot;plyr&quot;},controls:[&quot;play-large&quot;,&quot;play&quot;,&quot;progress&quot;,&quot;current-time&quot;,&quot;mute&quot;,&quot;volume&quot;,&quot;captions&quot;,&quot;fullscreen&quot;],i18n:{restart:&quot;Restart&quot;,rewind:&quot;Rewind {seektime} secs&quot;,play:&quot;Play&quot;,pause:&quot;Pause&quot;,forward:&quot;Forward {seektime} secs&quot;,played:&quot;played&quot;,buffered:&quot;buffered&quot;,currentTime:&quot;Current time&quot;,duration:&quot;Duration&quot;,volume:&quot;Volume&quot;,toggleMute:&quot;Toggle Mute&quot;,toggleCaptions:&quot;Toggle Captions&quot;,toggleFullscreen:&quot;Toggle Fullscreen&quot;,frameTitle:&quot;Player for {title}&quot;},types:{embed:[&quot;youtube&quot;,&quot;vimeo&quot;,&quot;soundcloud&quot;],html5:[&quot;video&quot;,&quot;audio&quot;]},urls:{vimeo:{api:&quot;https://cdn.plyr.io/froogaloop/1.0.1/plyr.froogaloop.js&quot;},youtube:{api:&quot;https://www.youtube.com/iframe_api&quot;},soundcloud:{api:&quot;https://w.soundcloud.com/player/api.js&quot;}},listeners:{seek:null,play:null,pause:null,restart:null,rewind:null,forward:null,mute:null,volume:null,captions:null,fullscreen:null},events:[&quot;ended&quot;,&quot;progress&quot;,&quot;stalled&quot;,&quot;playing&quot;,&quot;waiting&quot;,&quot;canplay&quot;,&quot;canplaythrough&quot;,&quot;loadstart&quot;,&quot;loadeddata&quot;,&quot;loadedmetadata&quot;,&quot;timeupdate&quot;,&quot;volumechange&quot;,&quot;play&quot;,&quot;pause&quot;,&quot;error&quot;,&quot;seeking&quot;,&quot;emptied&quot;]};return{setup:F,supported:S,loadSprite:C}}),function(){function e(e,t){t=t||{bubbles:!1,cancelable:!1,detail:void 0};var n=document.createEvent(&quot;CustomEvent&quot;);return n.initCustomEvent(e,t.bubbles,t.cancelable,t.detail),n}return&quot;function&quot;==typeof window.CustomEvent?!1:(e.prototype=window.Event.prototype,void(window.CustomEvent=e))}();</td>
      </tr>
</table>

  </div>

</div>

<button type="button" data-facebox="#jump-to-line" data-facebox-class="linejump" data-hotkey="l" class="hidden">Jump to Line</button>
<div id="jump-to-line" style="display:none">
  <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="" class="js-jump-to-line-form" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
    <input class="form-control linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" aria-label="Jump to line" autofocus>
    <button type="submit" class="btn">Go</button>
</form></div>

  </div>
  <div class="modal-backdrop"></div>
</div>


    </div>
  </div>

    </div>

        <div class="container site-footer-container">
  <div class="site-footer" role="contentinfo">
    <ul class="site-footer-links right">
        <li><a href="https://status.github.com/" data-ga-click="Footer, go to status, text:status">Status</a></li>
      <li><a href="https://developer.github.com" data-ga-click="Footer, go to api, text:api">API</a></li>
      <li><a href="https://training.github.com" data-ga-click="Footer, go to training, text:training">Training</a></li>
      <li><a href="https://shop.github.com" data-ga-click="Footer, go to shop, text:shop">Shop</a></li>
        <li><a href="https://github.com/blog" data-ga-click="Footer, go to blog, text:blog">Blog</a></li>
        <li><a href="https://github.com/about" data-ga-click="Footer, go to about, text:about">About</a></li>

    </ul>

    <a href="https://github.com" aria-label="Homepage" class="site-footer-mark" title="GitHub">
      <svg aria-hidden="true" class="octicon octicon-mark-github" height="24" version="1.1" viewBox="0 0 16 16" width="24"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59 0.4 0.07 0.55-0.17 0.55-0.38 0-0.19-0.01-0.82-0.01-1.49-2.01 0.37-2.53-0.49-2.69-0.94-0.09-0.23-0.48-0.94-0.82-1.13-0.28-0.15-0.68-0.52-0.01-0.53 0.63-0.01 1.08 0.58 1.23 0.82 0.72 1.21 1.87 0.87 2.33 0.66 0.07-0.52 0.28-0.87 0.51-1.07-1.78-0.2-3.64-0.89-3.64-3.95 0-0.87 0.31-1.59 0.82-2.15-0.08-0.2-0.36-1.02 0.08-2.12 0 0 0.67-0.21 2.2 0.82 0.64-0.18 1.32-0.27 2-0.27 0.68 0 1.36 0.09 2 0.27 1.53-1.04 2.2-0.82 2.2-0.82 0.44 1.1 0.16 1.92 0.08 2.12 0.51 0.56 0.82 1.27 0.82 2.15 0 3.07-1.87 3.75-3.65 3.95 0.29 0.25 0.54 0.73 0.54 1.48 0 1.07-0.01 1.93-0.01 2.2 0 0.21 0.15 0.46 0.55 0.38C13.71 14.53 16 11.53 16 8 16 3.58 12.42 0 8 0z"></path></svg>
</a>
    <ul class="site-footer-links">
      <li>&copy; 2016 <span title="0.10089s from github-fe117-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="https://github.com/site/terms" data-ga-click="Footer, go to terms, text:terms">Terms</a></li>
        <li><a href="https://github.com/site/privacy" data-ga-click="Footer, go to privacy, text:privacy">Privacy</a></li>
        <li><a href="https://github.com/security" data-ga-click="Footer, go to security, text:security">Security</a></li>
        <li><a href="https://github.com/contact" data-ga-click="Footer, go to contact, text:contact">Contact</a></li>
        <li><a href="https://help.github.com" data-ga-click="Footer, go to help, text:help">Help</a></li>
    </ul>
  </div>
</div>



    

    <div id="ajax-error-message" class="ajax-error-message flash flash-error">
      <svg aria-hidden="true" class="octicon octicon-alert" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M15.72 12.5l-6.85-11.98C8.69 0.21 8.36 0.02 8 0.02s-0.69 0.19-0.87 0.5l-6.85 11.98c-0.18 0.31-0.18 0.69 0 1C0.47 13.81 0.8 14 1.15 14h13.7c0.36 0 0.69-0.19 0.86-0.5S15.89 12.81 15.72 12.5zM9 12H7V10h2V12zM9 9H7V5h2V9z"></path></svg>
      <button type="button" class="flash-close js-flash-close js-ajax-error-dismiss" aria-label="Dismiss error">
        <svg aria-hidden="true" class="octicon octicon-x" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M7.48 8l3.75 3.75-1.48 1.48-3.75-3.75-3.75 3.75-1.48-1.48 3.75-3.75L0.77 4.25l1.48-1.48 3.75 3.75 3.75-3.75 1.48 1.48-3.75 3.75z"></path></svg>
      </button>
      Something went wrong with that request. Please try again.
    </div>


      
      <script crossorigin="anonymous" integrity="sha256-52zkLOd8k0WG98rL4k1Vbb5v79votTo5NkSxgZn3wpE=" src="https://assets-cdn.github.com/assets/frameworks-e76ce42ce77c934586f7cacbe24d556dbe6fefdbe8b53a393644b18199f7c291.js"></script>
      <script async="async" crossorigin="anonymous" integrity="sha256-Qnpk3C1XAs7SnAE9psXDYPqr67luWObUJ0IdRGaVYVA=" src="https://assets-cdn.github.com/assets/github-427a64dc2d5702ced29c013da6c5c360faabebb96e58e6d427421d4466956150.js"></script>
      
      
      
      
      
      
    <div class="js-stale-session-flash stale-session-flash flash flash-warn flash-banner hidden">
      <svg aria-hidden="true" class="octicon octicon-alert" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M15.72 12.5l-6.85-11.98C8.69 0.21 8.36 0.02 8 0.02s-0.69 0.19-0.87 0.5l-6.85 11.98c-0.18 0.31-0.18 0.69 0 1C0.47 13.81 0.8 14 1.15 14h13.7c0.36 0 0.69-0.19 0.86-0.5S15.89 12.81 15.72 12.5zM9 12H7V10h2V12zM9 9H7V5h2V9z"></path></svg>
      <span class="signed-in-tab-flash">You signed in with another tab or window. <a href="">Reload</a> to refresh your session.</span>
      <span class="signed-out-tab-flash">You signed out in another tab or window. <a href="">Reload</a> to refresh your session.</span>
    </div>
    <div class="facebox" id="facebox" style="display:none;">
  <div class="facebox-popup">
    <div class="facebox-content" role="dialog" aria-labelledby="facebox-header" aria-describedby="facebox-description">
    </div>
    <button type="button" class="facebox-close js-facebox-close" aria-label="Close modal">
      <svg aria-hidden="true" class="octicon octicon-x" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M7.48 8l3.75 3.75-1.48 1.48-3.75-3.75-3.75 3.75-1.48-1.48 3.75-3.75L0.77 4.25l1.48-1.48 3.75 3.75 3.75-3.75 1.48 1.48-3.75 3.75z"></path></svg>
    </button>
  </div>
</div>

  </body>
</html>

