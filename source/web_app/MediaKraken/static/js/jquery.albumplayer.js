(function($, window, document, undefined) {
    var AlbumPlayer = function(elem, options) {
	    this.$elem = $(elem);
        this.$elem.data('instance', this);
        this.init(options);
    };

    AlbumPlayer.prototype = {
        defaults: {
            audioButtonClass: 'album-player-button',
            autoPlay: null,
	    continuous: false,
            controlsClass: 'album-player-controls',
            extension: null,
            loadingClass: 'album-player-loading',
            loop: false,
            playerContainer: 'album-player-container',
            playingClass: 'album-player-playing',
            volume: 0.5,
        },

        isPlaying: false,

        init: function(options) {
            var scope = this,
                i = 0,
                ilen;
            //set defaults
            this.options = $.extend(true, {}, this.defaults, (options || {}));
            this.loadProxy = $.proxy(this.onLoaded, this);
            this.errorProxy = $.proxy(this.onError, this);
            this.endProxy = $.proxy(this.onEnded, this);
            this.$buttons = $("." + this.options.audioButtonClass);

            //listen for clicks on the controls
            $("." + this.options.controlsClass).on("click", function(event) {
                scope.updateTrackState(event);
                return false;
            });

            if (this.options.autoPlay) {
                this.play(this.options.autoPlay);
            }
        },

        pause: function() {
            this.audio.pause();
            this.$tgt.removeClass(this.options.playingClass);
            this.isPlaying = false;
        },

        play: function(element) {
            this.$tgt = typeof element === 'undefined' ? $('.' + this.options.audioButtonClass).eq(0) : element;
            this.currentTrack = this.getFileNameWithoutExtension(this.$tgt.attr("href"));
            this.isPlaying = true;
            this.$tgt.addClass(this.options.loadingClass);
            this.$buttons.removeClass(this.options.playingClass);
            // if audio already playing, pause and remove stream before starting new one
            if (this.audio) {
                this.audio.pause();
                this.removeListeners(this.audio);
            }
            this.audio = AV.Player.fromFile(this.$tgt.attr("href"));
//            this.audio = new Audio("");
            this.addListeners(this.audio);
//            this.audio.id = "audio";
//            this.audio.loop = this.options.loop ? "loop" : "";
//            this.audio.volume = this.options.volume;
//            this.audio.src = this.currentTrack + this.options.extension;
            this.audio.play();
        },

        playing: function() {
            return this.isPlaying;
        },

        resume: function() {
            this.audio.play();
            this.$tgt.addClass(this.options.playingClass);
            this.isPlaying = true;
        },

        updateTrackState: function(evt) {
            this.$tgt = $(evt.target);
            if (!this.$tgt.hasClass(this.options.audioButtonClass)) {
                return;
            }
            if (!this.audio || (this.audio && this.currentTrack !== this.getFileNameWithoutExtension(this.$tgt.attr("href")))) {
                this.play(this.$tgt);
            } else if (!this.isPlaying) {
                this.resume();
            } else {
                this.pause();
            }
        },

        addListeners: function(elem) {
            var el = $(elem);
            el.on('canplay', this.loadProxy);
            el.on('error', this.errorProxy);
            el.on('ended', this.endProxy);
        },

        removeListeners: function(elem) {
            var el = $(elem);
            el.off('canplay', this.loadProxy);
            el.off('error', this.errorProxy);
            el.off('ended', this.endProxy);
        },

        onLoaded: function() {
            this.$buttons.removeClass(this.options.loadingClass);
            this.$tgt.addClass(this.options.playingClass);

            this.audio.play();
        },

        onError: function() {
            this.$buttons.removeClass(this.options.loadingClass);
            if (this.isFlash) {
                this.removeListeners(window);
            } else {
                this.removeListeners(this.audio);
            }
        },

        onEnded: function() {
            this.isPlaying = false;
            this.$tgt.removeClass(this.options.playingClass);
            this.currentTrack = "";
            this.removeListeners(this.audio);
            if (this.options.continuous) {
                var $next = this.$tgt.next().length ? this.$tgt.next() : $(this.options.audioButtonClass).eq(0);
                this.play($next);
            }
        },

        getFileNameWithoutExtension: function(fileName) {
            //this function take a full file name and returns an extensionless file name
            //ex. entering foo.mp3 returns foo
            //ex. entering foo returns foo (no change)
            var fileNamePieces = fileName.split('.');
            fileNamePieces.pop();
            return fileNamePieces.join(".");
        }
    };

    $.fn.AlbumPlayer = function(options, args) {
        if (typeof options === 'string') {
            return this.each(function() {
                $(this).data('instance')[options](args);
            });
        } else {
            return this.each(function() {
                new AlbumPlayer(this, options);
            });
        }
    };

})(jQuery, window, document);
