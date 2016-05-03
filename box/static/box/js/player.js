/* Hearcloud player */
(function() {
  // Core variables
  var animateUi,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  // Once the document is ready 
  $(document).ready(function() {
    // Web Audio API setup
    var audio_context;
    if ($('#player').length !== 0) {
      if (typeof AudioContext !== "undefined") {
        audio_context = new AudioContext();
      } else if (typeof webkitAudioContext !== "undefined") {
        audio_context = new webkitAudioContext();
      } else {
        throw new Error('AudioContext not supported on your browser');
      }
      if (audio_context) {
        window.audio_context = audio_context;
        window.hearcloudplayer_audio = new HearcloudPlayerAudio(audio_context);
        window.hearcloudplayer_ui = new HearcloudPlayerUi();
        hearcloudplayer_ui.createDeck(hearcloudplayer_audio.state);
        return animateUi();
      }
    }
  });

  // UI Animation
  animateUi = function() {
      hearcloudplayer_ui.deck.deck_scope.draw(); // Draw track scope animation
      hearcloudplayer_ui.deck.deck_position.draw(); // Draw track position animation
      return requestAnimFrame(animateUi);
  };

  // requestAnimFrame
  window.requestAnimFrame = (function(callback) {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || function(callback) {
      return window.setTimeout(callback, 1000 / 60);
    };
  })();

/* ************************************************************************* */
  /* Class HearcloudPlayerAudio */
  this.HearcloudPlayerAudio = (function() {
    function HearcloudPlayerAudio(audio_context) {
      // Web Audio API Audio Context
      this.audio_context = audio_context;
      // State
      this.state = new HearcloudPlayerAudioState(this.audio_context);
      this.state.set_other_state(this.state);
      // Player itself
      this.deck = new HearcloudPlayerAudioDeck(this.state);
      // FX (Gain) and connections
      this.fx = new HearcloudPlayerAudioFX(this.audio_context);
      this.fx.plug(this.deck.processor);
      this.fx.connect(this.audio_context.destination);
    }

    return HearcloudPlayerAudio;
  })();

/* ************************************************************************* */
  /* Class HearcloudPlayerParameter */
  this.HearcloudPlayerParameter = (function() {
    function HearcloudPlayerParameter(default_value) {
      this.observers = [];
      this.value = default_value;
    }

    HearcloudPlayerParameter.prototype.add_listener = function(context, listener) {
      return this.observers.push([context, listener]);
    };

    HearcloudPlayerParameter.prototype.remove_listener = function(context, listener) {
      var index;
      index = this.observers.indexOf([context, listener]);
      return this.observers.splice(index, 1);
    };

    HearcloudPlayerParameter.prototype.notify = function() {
      var fun, _i, _len, _ref, _results;
      _ref = this.observers;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        fun = _ref[_i];
        _results.push(fun[1].call(fun[0], this.value));
      }
      return _results;
    };

    HearcloudPlayerParameter.prototype.change_value = function(new_value) {
      if (new_value !== this.value) {
        this.value = new_value;
        return this.notify();
      }
    };

    return HearcloudPlayerParameter;
  })();
/* ************************************************************************* */
/* Class HearcloudPlayerUi */
  this.HearcloudPlayerUi = (function() {
    function HearcloudPlayerUi() {
      this.controls_visible = new HearcloudPlayerParameter(false);
      window.addEventListener('drop', function(ev) {
        return ev.preventDefault();
      }, false);
      window.addEventListener('dragover', function(ev) {
        return ev.preventDefault();
      }, false);
    }

    HearcloudPlayerUi.prototype.createDeck = function(state) {
      return this.deck = new HearcloudPlayerUiDeck(state, ''); // CHECK second parameter
    };

    HearcloudPlayerUi.prototype.showControls = function() {
      $('#player').animate({
        height: 265
      }, {
        duration: 500
      });
      $('.deck').animate({
        height: 265
      }, 500);
      return $('.deck-controls').animate({
        height: 'show'
      }, 500);
    };

    HearcloudPlayerUi.prototype.hideControls = function() {
      $('#player').animate({
        height: 215
      }, {
        duration: 500
      });
      $('.deck').animate({
        height: 215
      }, 500);
      return $('.deck-controls').animate({
        height: 'hide'
      }, 500);
    };

    return HearcloudPlayerUi;

  })();

/* ************************************************************************* */
/* Class HearcloudPlayerAudioDeck */
  this.HearcloudPlayerAudioDeck = (function() {
    function HearcloudPlayerAudioDeck(state) {
      var audio_context, deck;
      this.state = state;
      this.buffer_size = this.state.buffer_size;
      audio_context = this.state.audio_context;
      if (audio_context.createScriptProcessor) {
        // size, inputs, outputs
        this.processor = audio_context.createScriptProcessor(this.buffer_size, 0, this.state.channels);
      } else {
        // size, inputs, outputs
        this.processor = audio_context.createJavaScriptNode(this.buffer_size, 0, this.state.channels);
      }
      deck = this;
      this.processor.onaudioprocess = function(event) {
        return deck.get_samples(event);
      };
      this.rate = 1;
      this.state.bpm.add_listener(this, this.update_bpm); // CHECK
      this.state.loaded.add_listener(this, this.update_bpm);
      this.zero_array = new Float32Array(this.buffer_size);
      this.beep_length = 882;
      this.beep_rate = 0.1;
      this.generate_beep();
      this.looping = false;
      this.loop_start = 0;
      this.loop_end = 0;
      this.state.looping.add_listener(this, this.update_loop);
      this.state.loop_start.add_listener(this, this.update_loop);
      this.state.loop_length.add_listener(this, this.update_loop);
      null;
    }

    HearcloudPlayerAudioDeck.prototype.generate_beep = function() {
      var run_down_size;
      this.beep = new Float32Array(this.beep_length);
      run_down_size = this.beep_length;
      while (--run_down_size >= 0) {
        this.beep[run_down_size] = Math.sin(run_down_size * this.beep_rate);
      }
      return null;
    };

    HearcloudPlayerAudioDeck.prototype.interpolate = function(input_channel, offset, alpha) {
      var c0, c1, c2, even1, even2, odd1, odd2, x0, x1, x2, x3, z;
      x0 = input_channel[offset];
      x1 = input_channel[offset + 1];
      x2 = input_channel[offset + 2];
      x3 = input_channel[offset + 3];
      z = alpha - 0.5;
      even1 = x2 + x1;
      odd1 = x2 - x1;
      even2 = x3 + x0;
      odd2 = x3 - x0;
      c0 = even1 * 0.32852206663814043 + even2 * 0.17147870380790242;
      c1 = odd1 * -0.35252373075274990 + odd2 * 0.45113687946292658;
      c2 = even1 * -0.240052062078895181 + even2 * 0.24004281672637814;
      return (c2 * z + c1) * z + c0;
    };

    HearcloudPlayerAudioDeck.prototype.connect = function(output) {
      this.processor.connect();
      return null;
    };

    HearcloudPlayerAudioDeck.prototype.update_bpm = function(new_bpm) {
      if (this.state.loaded.value) {
        this.rate = this.state.bpm.value / this.state.tune.bpm.value;
      }
      return null;
    };

    HearcloudPlayerAudioDeck.prototype.update_loop = function() {
      if (this.state.sound_loaded.value && this.state.looping.value) {
        if (!(this.loop_start === this.state.loop_start.value && this.loop_end === this.state.loop_end)) {
          this.state.update_looping_end();
          this.loop_start = this.state.loop_start.value;
          this.loop_end = this.state.loop_end;
          return this.looping = true;
        }
      } else {
        return this.looping = false;
      }
    };

    HearcloudPlayerAudioDeck.prototype.process_loop_samples = function(input_channels, output_channels) {
      var loop_length, position, samples_after_loop_start, samples_to_loop_end;
      position = this.state.position.value;
      loop_length = this.loop_end - this.loop_start;
      samples_to_loop_end = Math.floor((this.loop_end - position) / this.rate);
      samples_after_loop_start = this.buffer_size - samples_to_loop_end;
      if (samples_to_loop_end > (this.buffer_size * this.rate)) {
        this.process_samples(position, this.buffer_size, input_channels, 0, output_channels);
        return position + (this.buffer_size * this.rate);
      } else {
        this.process_samples(position, samples_to_loop_end, input_channels, 0, output_channels);
        if (this.loop_start < 0) {
          output_channels[0].set(this.zero_array);
          output_channels[1].set(this.zero_array);
        } else {
          this.process_samples(this.loop_start, samples_after_loop_start, input_channels, samples_to_loop_end, output_channels);
          // Fade out the end and fade in the start 20 samples
          if (samples_to_loop_end > 20 && samples_after_loop_start > 20) {
            this.fade_in(samples_to_loop_end, 20, output_channels);
            this.fade_out(samples_to_loop_end, 20, output_channels);
          }
        }
        return this.loop_start + (samples_after_loop_start * this.rate);
      }
    };

    HearcloudPlayerAudioDeck.prototype.fade_in = function(position, length, output_channels) {
      var end_left, end_right, i, step_left, step_right, value_left, value_right, _results;
      end_left = output_channels[0][position + length];
      end_right = output_channels[0][position + length];
      step_left = end_left / length;
      step_right = end_right / length;
      value_left = 0.0;
      value_right = 0.0;
      i = 0;
      _results = [];
      while (++i <= length) {
        output_channels[0][position + i] = value_left;
        output_channels[1][position + i] = value_right;
        value_left += step_left;
        _results.push(value_right += step_right);
      }
      return _results;
    };

    HearcloudPlayerAudioDeck.prototype.fade_out = function(position, length, output_channels) {
      var i, start_left, start_right, step_left, step_right, value_left, value_right, _results;
      start_left = output_channels[0][position - length];
      start_right = output_channels[1][position - length];
      step_left = start_left / length;
      step_right = start_right / length;
      value_left = start_left;
      value_right = start_right;
      i = 0;
      _results = [];
      while (++i <= length) {
        value_left -= step_left;
        value_right -= step_right;
        output_channels[0][position - i] = value_left;
        _results.push(output_channels[1][position - i] = value_right);
      }
      return _results;
    };

    HearcloudPlayerAudioDeck.prototype.process_samples = function(input_start, run_down_size, input_channels, output_start, output_channels) {
      var beat, beeping, destination_offset, sample_l, sample_r, source_offset, source_offset_float;
      beeping = this.state.beep.value;
      if (beeping) {
        beat = this.state.get_beep_beat(input_start - this.beep_length);
      }
      while (--run_down_size >= 0) {
        source_offset_float = input_start + (run_down_size * this.rate);
        source_offset = Math.round(source_offset_float);
        destination_offset = output_start + run_down_size;
        sample_l = input_channels[0][source_offset];
        sample_r = input_channels[1][source_offset];
        if (beeping && source_offset >= beat && source_offset < (beat + this.beep_length)) {
          output_channels[0][destination_offset] = (this.beep[source_offset - beat] + sample_l) / 2;
          output_channels[1][destination_offset] = (this.beep[source_offset - beat] + sample_r) / 2;
        } else {
          output_channels[0][destination_offset] = sample_l;
          output_channels[1][destination_offset] = sample_r;
        }
      }
      return null;
    };

    HearcloudPlayerAudioDeck.prototype.get_samples = function(event) {
      var edge_distance, end_position, input_channels, new_position, output_channels, position, sampling_distance;
      output_channels = new Array(this.state.channels);
      output_channels[0] = event.outputBuffer.getChannelData(0);
      output_channels[1] = event.outputBuffer.getChannelData(1);

      if (this.state.sound_loaded.value && this.state.playing.value) {
        position = this.state.position.value;
        input_channels = new Array(this.state.channels);
        input_channels[0] = this.state.buffer.getChannelData(0);
        input_channels[1] = this.state.buffer.getChannelData(1);

        // Dont sample beyond the end of input
        sampling_distance = this.state.buffer_size;
        end_position = (this.buffer_size * this.rate) + position;
        edge_distance = this.state.buffer.length - (end_position + 4);
        
        // If we are below 0 position, play nothing and increase the position like normal
        if (position < 0) {
          output_channels[0].set(this.zero_array);
          output_channels[1].set(this.zero_array);
          this.state.position.change_value(end_position);
        } else if (edge_distance <= 0) {
          // Stop playback if the end is reached
          this.state.playing.change_value(false);
          output_channels[0].set(this.zero_array);
          output_channels[1].set(this.zero_array);
          // If the end of the sample will take is over the loop threshold - loop around!
        } else if (this.looping && position < this.loop_end && position > this.loop_start) {
          new_position = this.process_loop_samples(input_channels, output_channels);
          this.state.position.change_value(new_position);
        } else {
          this.process_samples(position, this.buffer_size, input_channels, 0, output_channels);
          this.state.position.change_value((this.buffer_size * this.rate) + position);
        }
      } else {
        output_channels[0].set(this.zero_array);
        output_channels[1].set(this.zero_array);
      }

      output_channels = null;
      input_channels = null;
      return null;
    };

    return HearcloudPlayerAudioDeck;
  })();

/* ************************************************************************* */
/* Class HearcloudPlayerAudioFX */
  this.HearcloudPlayerAudioFX = (function() {
    function HearcloudPlayerAudioFX(audio_context) {
      this.audio_context = audio_context;
      this.gain_node = this.audio_context.createGain();
      this.gain_node.gain.value = 1;
      this.gain = new HearcloudPlayerParameter(50); // CHECK
      this.gain.add_listener(this, this.update_gain);
      // ... Connect here to create the chain if you add more FX
    }

    // Method to connect to an output
    HearcloudPlayerAudioFX.prototype.connect = function(output) {
      return this.gain_node.connect(output);
    };

    // Method to connect from an input
    HearcloudPlayerAudioFX.prototype.plug = function(input) {
      return input.connect(this.gain_node);
    };

    HearcloudPlayerAudioFX.prototype.update_gain = function(value) {
      return this.gain_node.gain.value = (value / 100) * 2;
    };

    HearcloudPlayerAudioFX.prototype.linear_to_db = function(linear) {
      if (linear < 50) {
        return -(this.db_to_linear(50.0 - linear));
      } else if (linear === 50) {
        return 0;
      } else {
        return this.db_to_linear(linear - 50.0);
      }
    };

    HearcloudPlayerAudioFX.prototype.db_to_linear = function(db) {
      return Math.pow(10, db / 30.0) - 1.0;
    };

    return HearcloudPlayerAudioFX;

  })();


/* ************************************************************************* */
/* Class HearcloudPlayerAudioSegment */
  this.HearcloudPlayerAudioSegment = (function() {
    function HearcloudPlayerAudioSegment(url) {
      this.url = url;
      this.file = null; // ArrayBuffer to hold downloaded segment
      this.buffer = null; // ArrayBuffer to hold decoded audio
      this.progress = new HearcloudPlayerParameter(0);
      this.downloaded = new HearcloudPlayerParameter(false);
      this.decoded = new HearcloudPlayerParameter(false);
      this.decoding = false;
      this.xhr = null;
    }

    HearcloudPlayerAudioSegment.prototype.download_file = function() {
      var segment;
      segment = this;
      segment.downloaded.change_value(false);
      segment.xhr = new XMLHttpRequest();
      segment.xhr.withCredentials = "true";
      segment.xhr.open('GET', segment.url, true);
      segment.xhr.responseType = 'arraybuffer';
      segment.xhr.onprogress = function(e) {
        return segment.progress.change_value(Math.round((e.loaded / e.total) * 100));
      };
      segment.xhr.onload = function(e) {
        if (segment.xhr.readyState !== 4) {
        } else {
          segment.file = segment.xhr.response;
          console.log(segment.xhr);
          segment.downloaded.change_value(true);
          return segment.xhr = null;
        }
      };
      return segment.xhr.send();
    };

    HearcloudPlayerAudioSegment.prototype.decode = function() {
      var segment;
      segment = this;
      segment.decoding = true;
      return window.audio_context.decodeAudioData(segment.file, function(buffer) {
        segment.buffer = buffer;
        segment.decoded.change_value(true);
        return segment.decoding = false;
      });
    };

    HearcloudPlayerAudioSegment.prototype.clear_buffer = function() {
      this.decoded.change_value(false);
      return this.buffer = null;
    };

    HearcloudPlayerAudioSegment.prototype.clear = function() {
      this.downloaded.change_value(false);
      this.progress.change_value(0);
      this.file = null;
      return this.clear_buffer();
    };

    return HearcloudPlayerAudioSegment;
  })();
/* ************************************************************************* */
/* Class HearcloudPlayerAudioSegmentBuffer */
  this.HearcloudPlayerAudioSegmentBuffer = (function() {
    function HearcloudPlayerAudioSegmentBuffer(data) {
      var finished_loading_callback, first_segment, local_segment, sb, segment_data, _i, _len;
      this.segments = [];
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        segment_data = data[_i];
        local_segment = {
          segment: new HearcloudPlayerAudioSegment(segment_data.url),
          length: segment_data.length
        };
        local_segment.segment.download_file();
        this.segments.push(local_segment);
      }
      first_segment = this.segments[0].segment;
      sb = this;
      finished_loading_callback = function() {
        first_segment.downloaded.remove_listener(sb, finished_loading_callback);
        return first_segment.decode();
      };
      first_segment.downloaded.add_listener(sb, finished_loading_callback);
    }

    HearcloudPlayerAudioSegmentBuffer.prototype.get_range = function(start_position, end_position) {
      var current_chunk, current_chunk_position, end_chunk, end_chunk_position, i, left_buffer, left_input_channel, next_chunk, return_buffer, return_length, right_buffer, right_input_channel, subarray_end, _i, _ref;
      current_chunk = this.get_chunk_number(start_position);
      current_chunk_position = this.get_chunk_position(start_position);
      end_chunk = this.get_chunk_number(end_position);
      end_chunk_position = this.get_chunk_position(end_position);
      // Decode next chunk if we reach half way through current one
      if (end_chunk === current_chunk && end_chunk_position > (this.segments[current_chunk].length / 2)) {
        next_chunk = current_chunk + 1;
        if (this.segments.length > next_chunk) {
          if (!(this.segments[next_chunk].segment.decoded.value || this.segments[next_chunk].segment.decoding)) {
            this.segments[next_chunk].segment.decode();
            // Clear old segments
            if (current_chunk > 0) {
              for (i = _i = 0, _ref = current_chunk - 1; _i <= _ref; i = _i += 1) {
                if (this.segments[i].segment.decoded.value) {
                  this.segments[i].segment.clear_buffer();
                }
              }
            }
          }
        } else {
          if (!(this.segments[0].segment.decoded.value || this.segments[0].segment.decoding)) {
            this.segments[0].segment.decode();
          }
        }
      }
      return_length = end_position - start_position;
      left_buffer = new Float32Array(return_length);
      right_buffer = new Float32Array(return_length);
      if (this.segments[current_chunk].segment.decoded.value) {
        left_input_channel = this.segments[current_chunk].segment.buffer.getChannelData(0);
        right_input_channel = this.segments[current_chunk].segment.buffer.getChannelData(1);
        subarray_end = current_chunk_position + return_length;
        if (subarray_end > left_input_channel.length) {
          subarray_end = left_input_channel.length;
        }
        left_buffer.set(left_input_channel.subarray(current_chunk_position, subarray_end));
        right_buffer.set(right_input_channel.subarray(current_chunk_position, subarray_end));
        if (current_chunk !== end_chunk) {
          left_input_channel = this.segments[end_chunk].segment.buffer.getChannelData(0);
          right_input_channel = this.segments[end_chunk].segment.buffer.getChannelData(1);
          left_buffer.set(left_input_channel.subarray(0, end_chunk_position));
          right_buffer.set(right_input_channel.subarray(0, end_chunk_position));
        }
        left_input_channel = null;
        right_input_channel = null;
      }
      return_buffer = new Array(2);
      return_buffer[0] = left_buffer;
      return_buffer[1] = right_buffer;
      left_buffer = null;
      right_buffer = null;
      return return_buffer;
    };

    HearcloudPlayerAudioSegmentBuffer.prototype.get_chunk_position = function(position) {
      var chunk_offset, offset, segment, segment_end, segment_offset, _i, _len, _ref;
      segment_offset = 0;
      segment_end = 0;
      chunk_offset = 0;
      _ref = this.segments;
      for (offset = _i = 0, _len = _ref.length; _i < _len; offset = ++_i) {
        segment = _ref[offset];
        segment_offset = segment_end;
        segment_end = segment_end + segment.length;
        if (position > segment_offset && position < segment_end) {
          chunk_offset = position - segment_offset;
          break;
        }
      }
      return chunk_offset;
    };

    HearcloudPlayerAudioSegmentBuffer.prototype.get_chunk_number = function(position) {
      var chunk, offset, segment, segment_end, segment_offset, _i, _len, _ref;
      segment_offset = 0;
      segment_end = 0;
      chunk = 0;
      _ref = this.segments;
      for (offset = _i = 0, _len = _ref.length; _i < _len; offset = ++_i) {
        segment = _ref[offset];
        segment_offset = segment_end;
        segment_end = segment_end + segment.length;
        if (position > segment_offset && position < segment_end) {
          chunk = offset;
          break;
        }
      }
      return chunk;
    };

    return HearcloudPlayerAudioSegmentBuffer;
  })();

/* ************************************************************************* */
/* Class HearcloudPlayerAudioState */
this.HearcloudPlayerAudioState = (function() {
    function HearcloudPlayerAudioState(audio_context) {
      this.audio_context = audio_context;
      this.buffer_size = 2048;
      this.channels = 2;

      // Position in audio buffer, in samples
      this.position = new HearcloudPlayerParameter(0);

      // Deck's bpm, used to calculate the playback rate
      this.bpm = new HearcloudPlayerParameter(128);

      // Looping parameters
      this.looping = new HearcloudPlayerParameter(false);
      this.loop_start = new HearcloudPlayerParameter(0);
      this.loop_end = 0;
      this.loop_length = new HearcloudPlayerParameter(8);
    
      // Playing?
      this.playing = new HearcloudPlayerParameter(false);

      // Synced start?
      this.synced_start = new HearcloudPlayerParameter(true);

      // Metronome type thing
      this.beep = new HearcloudPlayerParameter(false);
      
      // Samples per beat
      this.spb = 0;

      // Image
      this.image_loaded = new HearcloudPlayerParameter(false);
      this.canvas = document.createElement("canvas");
      this.canvas.height = 80;
      this.image = this.canvas.getContext("2d");

      // Sound
      this.sound_loaded = new HearcloudPlayerParameter(false);
      this.buffer = null;

      // Are we loading?
      this.loading = new HearcloudPlayerParameter(false);
      this.loaded = new HearcloudPlayerParameter(false);
      this.image_loaded.add_listener(this, this.finished_loading);
      this.sound_loaded.add_listener(this, this.generate_image);
      this.sound_loaded.add_listener(this, this.finished_loading);

      this.tune = null;

      this.looping.add_listener(this, this.update_looping_end);
      this.loop_start.add_listener(this, this.update_looping_end);
      this.loop_length.add_listener(this, this.update_looping_end);

      this.playing.add_listener(this, this.play);
    }

    HearcloudPlayerAudioState.prototype.set_other_state = function(state) {
      this.other_state = state;
      return this.other_state.bpm.add_listener(this, this.check_sync);
    };

    HearcloudPlayerAudioState.prototype.check_sync = function() {
      if (this.synced_start.value && this.playing.value && this.other_state.playing.value) {
        return this.bpm.change_value(this.other_state.bpm.value);
      }
    };

    HearcloudPlayerAudioState.prototype.play = function() {
      if (this.synced_start.value && this.playing.value && this.other_state.playing.value) {
        return this.sync();
      }
    };

    HearcloudPlayerAudioState.prototype.load = function(file) {
      var state, tune;
      this.unload();
      this.tune = new HearcloudPlayerModelTune(file);
      this.loading.change_value(true);
      state = this;
      tune = this.tune;
      return this.tune.loaded.add_listener(this, function() {
        state.decode_file(tune.buffer);
        tune.bpm.add_listener(state, state.beatgrid_update);
        return tune.first_beat.add_listener(state, state.get_first_beat);
      });
    };

    HearcloudPlayerAudioState.prototype.unload = function() {
      this.playing.change_value(false);
      this.looping.change_value(false);
      this.position.change_value(0);
      this.beep.change_value(false);
      this.loaded.change_value(false);
      if (this.tune) {
        this.tune.bpm.remove_listener(this, this.beatgrid_update);
        this.tune.first_beat.remove_listener(this, this.get_first_beat);
      }
      this.buffer = null;
      this.image_loaded.change_value(false);
      this.sound_loaded.change_value(false);
      return this.loading.change_value(false);
    };

    HearcloudPlayerAudioState.prototype.beatgrid_update = function() {
      this.get_spb();
      this.get_first_beat();
      if (!this.other_state.playing.value) {
        return this.bpm.change_value(this.tune.bpm.value);
      }
    };

    HearcloudPlayerAudioState.prototype.finished_loading = function() {
      if (this.image_loaded.value && this.sound_loaded.value) {
        this.loading.change_value(false);
        this.loaded.change_value(true);
        this.beatgrid_update();
        if (!this.other_state.playing.value) {
          return this.bpm.change_value(this.tune.bpm.value);
        }
      } else {
        return this.loading.change_value(true);
      }
    };

    HearcloudPlayerAudioState.prototype.decode_file = function(data) {
      var state;
      state = this;
      return window.audio_context.decodeAudioData(data, function(buffer) {
        state.buffer = buffer;
        return state.sound_loaded.change_value(true);
      });
    };

    HearcloudPlayerAudioState.prototype.get_rms = function(data) {
      var i, length, sum, value;
      sum = 0.0;
      value = 0.0;
      length = data.length;
      i = 0;
      while (++i < length) {
        value = Math.abs(data[i]);
        sum = sum + (value * value);
      }
      return Math.sqrt(sum / length);
    };

    HearcloudPlayerAudioState.prototype.generate_image = function(v) {
      var half_height, i, left_channel, left_max, left_scale, left_value, left_values, offset, pixels_in_file, pixels_per_minute, right_channel, right_max, right_scale, right_value, right_values, samples_per_pixel;
      if (!v) {
        return;
      }
      pixels_per_minute = 1200;
      samples_per_pixel = Math.floor((this.audio_context.sampleRate * 60) / pixels_per_minute);
      pixels_in_file = Math.floor(this.buffer.length / samples_per_pixel);
      this.canvas.width = pixels_in_file;
      left_channel = this.buffer.getChannelData(0);
      right_channel = this.buffer.getChannelData(1);
      left_values = [];
      left_max = 0.0;
      right_values = [];
      right_max = 0.0;
      i = 0;
      while (++i < pixels_in_file) {
        offset = i * samples_per_pixel;
        left_value = this.get_rms(left_channel.subarray(offset, offset + samples_per_pixel));
        if (left_value > left_max) {
          left_max = left_value;
        }
        left_values.push(left_value);
        right_value = this.get_rms(right_channel.subarray(offset, offset + samples_per_pixel));
        if (right_value > right_max) {
          right_max = right_value;
        }
        right_values.push(right_value);
      }
      half_height = this.canvas.height / 2;
      left_scale = half_height / left_max;
      right_scale = half_height / right_max;
      this.image.lineWidth = 1;
      this.image.strokeStyle = '#0080FF'; // Waveform stroke style
      i = 0;
      while (++i < pixels_in_file) {
        left_value = left_values[i] * left_scale;
        right_value = right_values[i] * right_scale;
        this.image.beginPath();
        this.image.moveTo(i, half_height - left_value);
        this.image.lineTo(i, half_height + right_value);
        this.image.stroke();
        this.image.closePath();
      }
      return this.image_loaded.change_value(true);
    };

    HearcloudPlayerAudioState.prototype.get_closest_beat = function(position, offset) {
      var closest_beat, nearest_beat, next_beat, offset_position, previous_beat, threshold;
      offset_position = position - this.first_beat_in_samples;
      nearest_beat = offset_position / this.spb;
      previous_beat = Math.floor(nearest_beat);
      next_beat = Math.ceil(nearest_beat);
      threshold = .01;
      if (Math.abs(next_beat - nearest_beat) < threshold) {
        nearest_beat = next_beat;
      } else if (Math.abs(previous_beat - nearest_beat) < threshold) {
        nearest_beat = previous_beat;
      }
      if (offset > 0) {
        closest_beat = Math.ceil(nearest_beat) * this.spb + this.first_beat_in_samples;
        offset = offset - 1;
      } else {
        closest_beat = Math.floor(nearest_beat) * this.spb + this.first_beat_in_samples;
        offset = offset + 1;
      }
      return Math.round(closest_beat + offset * this.spb);
    };

    HearcloudPlayerAudioState.prototype.start_loop = function(length_in_beats) {
      if (this.looping.value && (this.loop_length.value === length_in_beats)) {
        return this.looping.change_value(false);
      } else if (this.looping.value && (this.loop_length.value !== length_in_beats)) {
        return this.loop_length.change_value(length_in_beats);
      } else {
        this.loop_start.change_value(this.get_current_beat());
        this.loop_length.change_value(length_in_beats);
        return this.looping.change_value(true);
      }
    };

    HearcloudPlayerAudioState.prototype.move_loop_forward = function() {
      var loop_distance;
      if ((this.position.value > this.loop_start.value) && (this.position.value < this.loop_end)) {
        loop_distance = this.position.value - this.loop_start.value;
      }
      this.loop_start.change_value(this.loop_end);
      if (loop_distance) {
        return this.position.change_value(this.loop_start.value + loop_distance);
      }
    };

    HearcloudPlayerAudioState.prototype.move_loop_back = function() {
      var loop_distance;
      if ((this.position.value > this.loop_start.value) && (this.position.value < this.loop_end)) {
        loop_distance = this.position.value - this.loop_start.value;
      }
      this.loop_start.change_value(this.loop_start.value - (this.spb * this.loop_length.value));
      if (loop_distance) {
        return this.position.change_value(this.loop_start.value + loop_distance);
      }
    };

    HearcloudPlayerAudioState.prototype.update_looping_end = function() {
      return this.loop_end = ~~(this.loop_start.value + (this.spb * this.loop_length.value));
    };

    HearcloudPlayerAudioState.prototype.get_first_beat = function() {
      return this.first_beat_in_samples = this.tune.first_beat.value * this.audio_context.sampleRate;
    };

    // Samples per beat
    HearcloudPlayerAudioState.prototype.get_spb = function() {
      return this.spb = (60 / this.tune.bpm.value) * this.audio_context.sampleRate * 4;
    };

    // Nearest beat position
    HearcloudPlayerAudioState.prototype.get_nearest_beat = function() {
      return this.get_closest_beat(this.position.value, 1);
    };

    HearcloudPlayerAudioState.prototype.get_current_beat = function() {
      return this.get_closest_beat(this.position.value, -1);
    };

    HearcloudPlayerAudioState.prototype.get_beep_beat = function(position) {
      var beep_beat, beep_spb, offset_position;
      offset_position = position - this.first_beat_in_samples;
      beep_spb = this.spb / 4;
      beep_beat = Math.round(Math.round(offset_position / beep_spb) * beep_spb + this.first_beat_in_samples);
      return beep_beat;
    };

    HearcloudPlayerAudioState.prototype.sync = function() {
      var corrected_position, local_beat_distance, local_near_next, local_next_beat, local_previous_beat, other_beat_distance, other_beat_fraction, other_near_next, other_next_beat, other_previous_beat;
      if (this.loaded.value && this.playing.value && this.other_state.playing.value) {
        this.bpm.change_value(this.other_state.bpm.value);
        local_previous_beat = this.get_closest_beat(this.position.value, -1);
        local_next_beat = this.get_closest_beat(this.position.value, 1);
        if (local_previous_beat === local_next_beat) {
          local_next_beat = this.get_closest_beat(this.position.value, 2);
        }
        other_previous_beat = this.other_state.get_closest_beat(this.other_state.position.value, -1);
        other_next_beat = this.other_state.get_closest_beat(this.other_state.position.value, 1);
        if (other_previous_beat === other_next_beat) {
          other_next_beat = this.other_state.get_closest_beat(this.other_state.position.value, 2);
        }
        local_beat_distance = Math.abs(local_next_beat - local_previous_beat);
        other_beat_distance = Math.abs(other_next_beat - other_previous_beat);
        other_beat_fraction = (this.other_state.position.value - other_previous_beat) / other_beat_distance;
        local_near_next = local_next_beat - this.position.value <= this.position.value - local_previous_beat;
        other_near_next = other_next_beat - this.other_state.position.value <= this.other_state.position.value - other_previous_beat;
        if (local_near_next === other_near_next) {
          corrected_position = local_previous_beat + other_beat_fraction * local_beat_distance;
        } else if (local_near_next && !other_near_next) {
          corrected_position = local_next_beat + other_beat_fraction * local_beat_distance;
        } else {
          local_previous_beat = this.get_closest_beat(this.position.value, -2);
          corrected_position = local_previous_beat + other_beat_fraction * local_beat_distance;
        }
        return this.position.change_value(corrected_position);
      }
    };

    return HearcloudPlayerAudioState;
  })();

/* ************************************************************************* */
/* Class HearcloudPlayerModelTune */
  this.HearcloudPlayerModelTune = (function() {
    function HearcloudPlayerModelTune(file) {
      var reader, tune;

      this.hash = null;
      this.original_bpm = 128;
      this.bpm = new HearcloudPlayerParameter(128);
      this.bpm.add_listener(this, this.check_minimum_bpm);

      this.original_first_beat = 0;
      this.first_beat = new HearcloudPlayerParameter(0);
      this.buffer = null;
      this.length = 0;
      this.loaded = new HearcloudPlayerParameter(false);

      //this.sha_worker = new Worker('https://cdn.rawgit.com/srijs/rusha/master/rusha.min.js');
      this.sha_worker = new Worker('/rusha.js')
      tune = this;

      this.sha_worker.addEventListener('message', function(e) {
        tune.hash = e.data.hash;
        return tune.load();
      }, false);

      this.name = new HearcloudPlayerParameter(file.name);
      this.saved = new HearcloudPlayerParameter(true);

      reader = new FileReader();
      reader.onload = function(evt) {
        tune.sha_worker.postMessage({
          id: 'test',
          data: evt.target.result
        });
        return tune.buffer = evt.target.result;
      };
      reader.readAsArrayBuffer(file);
    }

    HearcloudPlayerModelTune.prototype.check_minimum_bpm = function() {
      if (this.bpm.value < 5.0) {
        return this.bpm.change_value(5.0);
      }
    };

    HearcloudPlayerModelTune.prototype.length_to_time = function() {
      var minutes, seconds;
      minutes = (this.length / 44100) / 60;
      seconds = Math.round((minutes - Math.floor(minutes)) * 60).toString();
      if (seconds.length === 1) {
        seconds = '0' + seconds;
      }
      return "" + (Math.floor(minutes)) + ":" + seconds;
    };

    HearcloudPlayerModelTune.prototype.save = function() {
      var data;
      this.saved.change_value(false);
      data = {
        first_beat: this.first_beat.value,
        bpm: this.bpm.value
      };
      localStorage[this.hash] = JSON.stringify(data);
      this.original_bpm = this.bpm.value;
      this.original_first_beat = this.first_beat.value;
      return this.saved.change_value(true);
    };

    HearcloudPlayerModelTune.prototype.load = function() {
      var data;
      if (localStorage[this.hash]) {
        data = JSON.parse(localStorage[this.hash]);
        this.bpm.change_value(data.bpm);
        this.first_beat.change_value(data.first_beat);
        this.original_bpm = data.bpm;
        this.original_first_beat = data.first_beat;
      }
      return this.loaded.change_value(true);
    };

    return HearcloudPlayerModelTune;
  })();

/* ************************************************************************* */
/* Class HearcloudPlayerUiButton */
  this.HearcloudPlayerUiButton = (function() {
    function HearcloudPlayerUiButton(container, width, height) {
      var button;
      this.container = container;
      this.width = width;
      this.height = height;

      this.hovering = false;

      this.graphic_context = this.container.getContext("2d");

      this.container.width = this.width;
      this.container.height = this.height;

      this.draw();
      button = this;
      $(this.container).bind("click", this.click);
      $(this.container).bind("mouseover", function() {
        button.hovering = true;
        return button.draw();
      });
      $(this.container).bind("mouseout", function() {
        button.hovering = false;
        return button.draw();
      });
    }

    HearcloudPlayerUiButton.prototype.draw = function() {
      this.graphic_context.clearRect(0, 0, this.width, this.height);
      // Draw background
      this.background = this.graphic_context.createLinearGradient(0, 0, 0, this.container.height);
      if (this.hovering) {
        this.background.addColorStop(0, style.adjust(style.button_active_background, 20));
        this.background.addColorStop(0.5, style.button_active_background);
        this.foreground = style.button_active_foreground;
      } else if (this.alternate) {
        this.background.addColorStop(1, style.adjust(style.button_alternate_background, 50));
        this.background.addColorStop(0.5, style.button_alternate_background);
        this.foreground = style.button_foreground;
      } else {
        this.background.addColorStop(0, style.adjust(style.button_background, 20));
        this.background.addColorStop(0.5, style.button_background);
        this.foreground = style.button_foreground;
      }
      this.border = this.graphic_context.createLinearGradient(0, 0, 0, this.container.height);
      this.border.addColorStop(0, 'rgba(255,255,255,0.2)');
      this.border.addColorStop(0.5, 'rgba(0,0,0,0.2)');
      this.graphic_context.beginPath();
      this.graphic_context.rect(1.5, 1.5, this.width - 3, this.height - 3);
      this.graphic_context.closePath();
      this.graphic_context.fillStyle = this.background;
      this.graphic_context.fill();
      this.graphic_context.lineWidth = 1;
      this.graphic_context.strokeStyle = this.border;
      this.graphic_context.stroke();
      this.graphic_context.beginPath();
      this.graphic_context.rect(0.5, 0.5, this.width - 1, this.height - 1);
      this.graphic_context.closePath();
      this.graphic_context.lineWidth = 1;
      this.graphic_context.strokeStyle = 'rgba(0,0,0,0.3)';
      return this.graphic_context.stroke();
    };

    return HearcloudPlayerUiButton;

  })();
/* ************************************************************************* */
/* BUTTONS */
/* ************************************************************************* */
/* Play Button */
  this.HearcloudPlayerUiButtonPlay = (function(_super) {
    __extends(HearcloudPlayerUiButtonPlay, _super);

    function HearcloudPlayerUiButtonPlay(container, param) {
      this.container = container;
      this.param = param;
      this.click = __bind(this.click, this);

      // Size: 60x30
      HearcloudPlayerUiButtonPlay.__super__.constructor.call(this, this.container, 60, 30);
      this.param.add_listener(this, this.draw);
    }

    HearcloudPlayerUiButtonPlay.prototype.click = function(e) {
      e.preventDefault();
      if (this.param.value) {
        return this.param.change_value(false);
      } else {
        return this.param.change_value(true);
      }
    };

    HearcloudPlayerUiButtonPlay.prototype.draw = function() {
      HearcloudPlayerUiButtonPlay.__super__.draw.call(this);

      // Draw graphic
      this.graphic_context.fillStyle = this.foreground;
      if (this.param.value) {
        this.graphic_context.beginPath();
        this.graphic_context.moveTo(20, 7);
        this.graphic_context.lineTo(28, 7);
        this.graphic_context.lineTo(28, 23);
        this.graphic_context.lineTo(20, 23);
        this.graphic_context.closePath();
        this.graphic_context.fill();
        this.graphic_context.beginPath();
        this.graphic_context.moveTo(32, 7);
        this.graphic_context.lineTo(40, 7);
        this.graphic_context.lineTo(40, 23);
        this.graphic_context.lineTo(32, 23);
        this.graphic_context.closePath();
        return this.graphic_context.fill();
      } else {
        this.graphic_context.beginPath();
        this.graphic_context.moveTo(20, 7);
        this.graphic_context.lineTo(40, 15);
        this.graphic_context.lineTo(20, 23);
        this.graphic_context.closePath();
        return this.graphic_context.fill();
      }
    };

    return HearcloudPlayerUiButtonPlay;

  })(HearcloudPlayerUiButton);
/* ************************************************************************* */
/* Class HearcloudPlayerUiScope */
  this.HearcloudPlayerUiScope = (function() {
    function HearcloudPlayerUiScope(container, state) {
      this.container = container;
      this.state = state;
      this.param_updated = __bind(this.param_updated, this);
      this.snap = __bind(this.snap, this);
      this.update_width = __bind(this.update_width, this);
      this.options = {
        width: 390,
        height: 80,
        background_style: 'rgba(0,0,0,1)',
        label_font: style.label_font,
        default_value: 0
      };
      this.graphic_context = this.container.getContext("2d");
      this.graphic_context.imageSmoothingEnabled = true;
      this.graphic_context.mozImageSmoothingEnabled = true;
      this.graphic_context.imageSmoothingEnabled = true;
      this.container.width = this.options.width;
      this.container.height = this.options.height;
      this.center = Math.round(this.container.width / 2) + 0.5;
      this.image = new Image();
      this.image_loaded = false;
      this.rotations_since_started = 1;
      this.sample_rate = this.state.audio_context.sampleRate;
      this.draw();
      $(this.container).bind("click", this.snap);
    }

    HearcloudPlayerUiScope.prototype.update_width = function(width) {
      this.options.width = width;
      this.container.width = width;
      return this.center = Math.round(width / 2) + 0.5;
    };

    HearcloudPlayerUiScope.prototype.samples_to_pixels = function(position_value) {
      var position_in_pixels, position_in_seconds;
      position_in_seconds = position_value / this.sample_rate;
      return position_in_pixels = position_in_seconds * 20;
    };

    HearcloudPlayerUiScope.prototype.pixels_to_samples = function(pixel_value) {
      var position_in_samples, position_in_seconds;
      position_in_seconds = pixel_value / 20;
      return position_in_samples = position_in_seconds * this.sample_rate;
    };

    HearcloudPlayerUiScope.prototype.calculate_nearest_beat = function(pixel_position) {
      var first_beat_in_samples, global_sample_position, offset_sample_position, sample_position, spacing_in_samples;
      if (this.state.loaded.value) {
        // Assuming first beat value is in seconds
        first_beat_in_samples = this.state.tune.first_beat.value * this.sample_rate;
        sample_position = this.pixels_to_samples(pixel_position - this.center);
        global_sample_position = this.state.position.value + sample_position;
        offset_sample_position = global_sample_position - first_beat_in_samples;
        spacing_in_samples = (60 / this.state.tune.bpm.value) * this.sample_rate * 4;
        this.nearest_beat = Math.round(offset_sample_position / spacing_in_samples);
        return this.nearest_beat_position = (this.nearest_beat * spacing_in_samples) + first_beat_in_samples;
      }
    };

    HearcloudPlayerUiScope.prototype.snap = function(e) {
      e.preventDefault();
      this.cursor_x = e.offsetX - 5;
      this.calculate_nearest_beat(this.cursor_x);
      this.state.position.change_value(this.nearest_beat_position);
      this.state.sync();
      return false;
    };

    HearcloudPlayerUiScope.prototype.get_spacing = function() {
      return (1200 / this.state.tune.bpm.value) * 4;
    };

    HearcloudPlayerUiScope.prototype.draw = function() {
      var beat_count, beat_count_unclean, bg_gradient, bitmap_offset, first_beat, first_marker, height, i, last_marker, local_position, loop_end, loop_start, rotation, spacing, width, x, _i, _j;
      width = this.container.width;
      height = this.container.height;
      this.graphic_context.clearRect(0, 0, width, height);
      bg_gradient = this.graphic_context.createLinearGradient(0, 0, 0, height);
      bg_gradient.addColorStop(0.5, 'rgba(0, 0, 0, 0.6)');
      bg_gradient.addColorStop(1, 'rgba(0, 0, 0, 0.2)');
      this.graphic_context.fillStyle = bg_gradient;
      this.graphic_context.fillRect(0, 0, width, height);
      // If we have stuff loaded on the deck
      if (this.state.loaded.value) {
        local_position = ~~(this.samples_to_pixels(this.state.position.value));
        bitmap_offset = this.center - local_position;
        spacing = this.get_spacing();
        // Draw waveform
        if (this.state.image_loaded.value) {
          this.graphic_context.drawImage(this.state.canvas, bitmap_offset, 0);
        }
        // Draw looping region
        if (this.state.looping.value) {
          loop_start = bitmap_offset + this.samples_to_pixels(this.state.loop_start.value);
          loop_end = this.samples_to_pixels(this.state.loop_end - this.state.loop_start.value);
          this.graphic_context.fillStyle = 'rgba(190,214,48,0.3)';
          this.graphic_context.fillRect(loop_start, 0, loop_end, height);
        }
        first_beat = this.samples_to_pixels(this.state.tune.first_beat.value * this.sample_rate);
        first_marker = (this.center - local_position + first_beat) % spacing;
        last_marker = width - first_marker + spacing;
        beat_count_unclean = ((local_position - first_beat) - this.center) / spacing;
        if (beat_count_unclean < 0) {
          beat_count = Math.ceil(beat_count_unclean);
        } else {
          beat_count = Math.floor(beat_count_unclean);
        }
        for (x = _i = first_marker; spacing > 0 ? _i <= last_marker : _i >= last_marker; x = _i += spacing) {
          this.graphic_context.beginPath();
          this.graphic_context.moveTo(x, 0);
          this.graphic_context.lineTo(x, height);
          if (beat_count !== 0) {
            // Draw 1/4 beat
            this.graphic_context.strokeStyle = 'rgba(255,202,5,0.2)';
            this.graphic_context.closePath();
            this.graphic_context.stroke();
          } else {
            // Draw first beat
            this.graphic_context.strokeStyle = 'rgba(255,255,255,1)';
            this.graphic_context.closePath();
            this.graphic_context.stroke();
            // Draw a little flag
            this.graphic_context.fillStyle = 'rgba(255,255,255,1)';
            this.graphic_context.beginPath();
            this.graphic_context.moveTo(x, 0);
            this.graphic_context.lineTo(x + 4.5, 4.5);
            this.graphic_context.lineTo(x, 9);
            this.graphic_context.closePath();
            this.graphic_context.fill();
          }
          beat_count++;
        }
        // Draw center line
        this.graphic_context.beginPath();
        this.graphic_context.moveTo(this.center, 10);
        this.graphic_context.lineTo(this.center, height - 10);
        this.graphic_context.closePath();
        this.graphic_context.strokeStyle = 'rgba(240,90,35,1)';
        this.graphic_context.stroke();
      } else if (this.state.loading.value) {
        this.graphic_context.translate(this.center, height / 2);
        this.graphic_context.strokeStyle = "rgba(255,255,255,0.05)";
        this.graphic_context.lineWidth = 5;
        this.graphic_context.beginPath();
        this.graphic_context.arc(0, 0, 35, 0, Math.PI * 2, true);
        this.graphic_context.closePath();
        this.graphic_context.stroke();
        rotation = this.rotations_since_started / 100;
        this.graphic_context.rotate(rotation);
        for (i = _j = 0; _j <= 2; i = ++_j) {
          this.graphic_context.rotate(Math.PI * 2 / 3);
          this.graphic_context.beginPath();
          this.graphic_context.moveTo(20, 0);
          this.graphic_context.lineTo(32, 0);
          this.graphic_context.closePath();
          this.graphic_context.stroke();
        }
        this.rotations_since_started++;
        this.graphic_context.setTransform(1, 0, 0, 1, 0, 0);
        this.graphic_context.font = this.options.label_font;
        this.graphic_context.textAlign = 'center';
        this.graphic_context.textBaseline = 'middle';
        this.graphic_context.fillStyle = style.button_foreground;
        this.graphic_context.fillText("Processing", this.center, height / 2);
        this.graphic_context.lineWidth = 1;
      } else {
        this.graphic_context.font = this.options.label_font;
        this.graphic_context.textAlign = 'center';
        this.graphic_context.textBaseline = 'middle';
        this.graphic_context.fillStyle = style.button_foreground;
        this.graphic_context.fillText("Drop an audio file here to start", this.center, height / 2);
      }
      // Draw shadow stroke
      this.graphic_context.beginPath();
      this.graphic_context.moveTo(0, 0);
      this.graphic_context.lineTo(width, 0);
      this.graphic_context.strokeStyle = 'rgba(0,0,0,0.3)';
      this.graphic_context.stroke();
      this.graphic_context.closePath();
      // Draw highlight stroke
      this.graphic_context.beginPath();
      this.graphic_context.moveTo(0, height - 0.5);
      this.graphic_context.lineTo(width, height - 0.5);
      this.graphic_context.strokeStyle = 'rgba(255,255,255,0.2)';
      this.graphic_context.stroke();
      this.graphic_context.closePath();
      return null;
    };

    HearcloudPlayerUiScope.prototype.param_updated = function(new_value) {
      return this.draw();
    };

    return HearcloudPlayerUiScope;
  })();
/* ************************************************************************* */
/* Class HearcloudPlayerUiPosition */
  this.HearcloudPlayerUiPosition = (function() {
    function HearcloudPlayerUiPosition(container, state) {
      this.container = container;
      this.state = state;
      this.click = __bind(this.click, this);
      this.update_width = __bind(this.update_width, this);

      this.options = {
        width: 390,
        height: 10
      };

      this.graphic_context = this.container.getContext("2d");
      this.container.width = this.options.width;
      this.container.height = this.options.height;

      this.draw();

      $(this.container).bind("mousedown", this.click);
    }

    HearcloudPlayerUiPosition.prototype.update_width = function(width) {
      this.options.width = width;
      this.container.width = this.options.width;
      return this.draw();
    };

    HearcloudPlayerUiPosition.prototype.click = function(e) {
      var offset;
      e.preventDefault();
      if (this.state.loaded.value) {
        offset = (e.offsetX - 5) / this.options.width;
        offset = Math.min(offset, 1);
        offset = Math.max(offset, 0);
        this.state.position.change_value(this.state.buffer.length * offset);
        return this.state.sync();
      }
    };

    HearcloudPlayerUiPosition.prototype.draw = function() {
      var height, progress_width, width;
      width = this.container.width;
      height = this.container.height;

      this.graphic_context.clearRect(0, 0, width, height);
      this.graphic_context.fillStyle = style.button_background;
      this.graphic_context.fillRect(0, 0, width, height);

      if (this.state.loaded.value) {
        progress_width = width * (this.state.position.value / this.state.buffer.length);
        this.graphic_context.fillStyle = style.button_foreground;
        this.graphic_context.fillRect(0, 0, progress_width, height);
      }

      // Draw shadow stroke
      this.graphic_context.beginPath();
      this.graphic_context.moveTo(0, 0.5);
      this.graphic_context.lineTo(width, 0.5);
      this.graphic_context.strokeStyle = 'rgba(0,0,0,0.3)';
      this.graphic_context.stroke();
      this.graphic_context.closePath();

      // Draw highlight stroke
      this.graphic_context.beginPath();
      this.graphic_context.moveTo(0, height - 0.5);
      this.graphic_context.lineTo(width, height - 0.5);
      this.graphic_context.strokeStyle = 'rgba(255,255,255,0.2)';
      this.graphic_context.stroke();
      return this.graphic_context.closePath();
    };

    return HearcloudPlayerUiPosition;
  })();
/* ************************************************************************* */
/* Class HearcloudPlayerUiLooper */
  this.HearcloudPlayerUiLooper = (function() {
    function HearcloudPlayerUiLooper(container, state) {
      this.container = container;
      this.state = state;
      this.hover_end = __bind(this.hover_end, this);
      this.hover = __bind(this.hover, this);
      this.click = __bind(this.click, this);

      this.options = {
        width: 278,
        height: 30
      };

      this.graphic_context = this.container.getContext("2d");
      this.container.width = this.options.width;
      this.container.height = this.options.height;

      // CSS Margin left offset
      this.offset = $(this.container).css("margin-left").replace("px", "");

      // Looper Buttons: move loop back/forward and loop size
      this.buttons = [
        {
          x: 0,
          y: 0,
          label: '<',
          value: 'back'
        }, {
          x: 31,
          y: 0,
          label: '1/4',
          value: 0.25
        }, {
          x: 62,
          y: 0,
          label: '1/2',
          value: 0.5
        }, {
          x: 93,
          y: 0,
          label: '1',
          value: 1
        }, {
          x: 124,
          y: 0,
          label: '2',
          value: 2
        }, {
          x: 155,
          y: 0,
          label: '4',
          value: 4
        }, {
          x: 186,
          y: 0,
          label: '8',
          value: 8
        }, {
          x: 217,
          y: 0,
          label: '16',
          value: 16
        }, {
          x: 248,
          y: 0,
          label: '>',
          value: 'forward'
        }
      ];
      this.draw();
      $(this.container).bind("mousedown", this.click);
      $(this.container).bind("mouseover mousemove", this.hover);
      $(this.container).bind("mouseout", this.hover_end);
    }

    HearcloudPlayerUiLooper.prototype.clear = function() {
      return this.graphic_context.clearRect(0, 0, this.container.width, this.container.height);
    };

    HearcloudPlayerUiLooper.prototype.click = function(e) {
      var button, button_key;
      e.preventDefault();
      button_key = this.get_current_button(e);
      button = this.buttons[button_key];
      if (button.value === 'forward') {
        return this.state.move_loop_forward();
      } else if (button.value === 'back') {
        return this.state.move_loop_back();
      } else {
        return this.state.start_loop(button.value);
      }
    };

    HearcloudPlayerUiLooper.prototype.hover = function(e) {
      this.hovering = true;
      this.current_button = this.get_current_button(e);
      return this.draw();
    };

    HearcloudPlayerUiLooper.prototype.get_current_button = function(mouse_event) {
      var button, cursor_x, key, _i, _len, _ref;
      cursor_x = mouse_event.offsetX;
      _ref = this.buttons;
      for (key = _i = 0, _len = _ref.length; _i < _len; key = ++_i) {
        button = _ref[key];
        if (cursor_x >= button.x && cursor_x <= button.x + 31) {
          return key;
        }
      }
    };

    HearcloudPlayerUiLooper.prototype.hover_end = function(e) {
      this.hovering = false;
      return this.draw();
    };

    // Draw all
    HearcloudPlayerUiLooper.prototype.draw = function() {
      var button, key, _i, _len, _ref, _results;
      this.clear();
      _ref = this.buttons;
      _results = [];
      for (key = _i = 0, _len = _ref.length; _i < _len; key = ++_i) {
        button = _ref[key];
        if (this.hovering && this.current_button === key) {
          _results.push(this.draw_button(button.label, button.x, button.y, style.button_active_background));
        } else if (this.state.looping.value && this.state.loop_length.value === button.value) {
          _results.push(this.draw_button(button.label, button.x, button.y, style.button_active_background));
        } else {
          _results.push(this.draw_button(button.label, button.x, button.y, style.button_background));
        }
      }
      return _results;
    };

    // Draw one loop button
    HearcloudPlayerUiLooper.prototype.draw_button = function(label, x, y, background) {
      var background_gradient, border;

      background_gradient = this.graphic_context.createLinearGradient(0, 0, 0, this.container.height);
      background_gradient.addColorStop(0, style.adjust(background, 20));
      background_gradient.addColorStop(0.5, background);

      border = this.graphic_context.createLinearGradient(0, 0, 0, this.container.height);
      border.addColorStop(0, 'rgba(255,255,255,0.2)');
      border.addColorStop(0.5, 'rgba(0,0,0,0.2)');

      // Draw bg
      this.graphic_context.fillStyle = background_gradient;
      this.graphic_context.beginPath();
      this.graphic_context.rect(x + 1.5, y + 1.5, 27, 27);
      this.graphic_context.closePath();
      this.graphic_context.fillStyle = background_gradient;
      this.graphic_context.fill();
      this.graphic_context.lineWidth = 1;
      this.graphic_context.strokeStyle = border;
      this.graphic_context.stroke();

      this.graphic_context.beginPath();
      this.graphic_context.rect(x + 0.5, y + 0.5, 29, 29);
      this.graphic_context.closePath();
      this.graphic_context.lineWidth = 1;
      this.graphic_context.strokeStyle = 'rgba(0,0,0,0.3)';
      this.graphic_context.stroke();

      // Draw label
      this.graphic_context.font = style.label_font;
      this.graphic_context.textAlign = 'center';
      this.graphic_context.textBaseline = 'middle';
      this.graphic_context.fillStyle = style.button_foreground;
      return this.graphic_context.fillText(label, x + 15, y + 15);
    };

    return HearcloudPlayerUiLooper;
  })();
/* ************************************************************************* */
/* Class HearcloudPlayerUiDeck */
  this.HearcloudPlayerUiDeck = (function() {
    function HearcloudPlayerUiDeck(state, prefix) {
      var dragging;
      this.state = state;
      this.prefix = prefix;
      this.resize = __bind(this.resize, this);

      // id="deck-scope"
      this.deck_scope = new HearcloudPlayerUiScope($("#" + "deck-scope")[0], state);
      // id="deck-position"
      this.deck_position = new HearcloudPlayerUiPosition($("#" + "deck-position")[0], state);
      // id="deck-play-button"
      this.deck_play_button = new HearcloudPlayerUiButtonPlay($("#" + "deck-play-button")[0], state.playing);
      // id="deck-looper"
      this.looper = new HearcloudPlayerUiLooper($("#" + "deck-looper")[0], state);
      // id="deck"
      $("#" + "deck").data('state', this.state);

      // Select track to play
      $(".btn-play-song").click(function(){
        var song_url;
        song_url = $(this).attr("songurl");
        var xhr = new XMLHttpRequest();
        xhr.open('GET', song_url, true);
        xhr.responseType = 'arraybuffer';
        xhr.onload = function() {
            if (this.status == 200) {
                console.log(xhr.response);
            }
        };
        xhr.send();
        /*ev.stopPropagation();
        ev.preventDefault();
        if (ev.dataTransfer.files.length > 0) {
          $(this).data('state').load(ev.dataTransfer.files[0]);
        }
        $(this).removeClass('lightup');
        return dragging = 0;*/
      });

      /*$(window).resize(this.resize);
      $(window).load(this.resize);

      this.state.loaded.add_listener(this, this.update_title);*/
    }

    // CHECK: ARTIST - TITLE
    HearcloudPlayerUiDeck.prototype.update_title = function() {
      if (this.state.loaded.value) {
        return $("#" + this.prefix + "-deck-info").text(this.state.tune.name.value);
      } else {
        return $("#" + this.prefix + "-deck-info").text(''); // No tittle on first load
      }
    };

    HearcloudPlayerUiDeck.prototype.resize = function() {
      var new_width;
      new_width = Math.floor(($('#player').innerWidth() - 140) / 2);
      this.deck_scope.update_width(new_width - 10);
      this.deck_position.update_width(new_width - 10);
      return $("#" + this.prefix + "-deck").width(new_width);
    };

    return HearcloudPlayerUiDeck;

  })();
/* ************************************************************************* */
/* Class HearcloudPlayerUiSlider */
  this.HearcloudPlayerUiSlider = (function() {
    function HearcloudPlayerUiSlider(container, options) {
      var defaults;
      this.container = container;
      this.change_value = __bind(this.change_value, this);
      this.scroll = __bind(this.scroll, this);
      this.startDrag = __bind(this.startDrag, this);
      this.resetPosition = __bind(this.resetPosition, this);

      defaults = {
        width: 120,
        height: 30,
        minimum: 0,
        maximum: 100,
        default_value: 50,
        snapping: true,
        on_change: function() {}
      };

      this.options = $.extend({}, defaults, options);

      this.value = this.options.default_value;
      this.graphic_context = this.container.getContext("2d");

      this.container.width = this.options.width;
      this.container.height = this.options.height;

      this.draw();
      $(this.container).bind("mousedown", this.startDrag);
      $(this.container).bind("dblclick", this.resetPosition);
      $(this.container).bind("mousewheel", this.scroll);
    }

    HearcloudPlayerUiSlider.prototype.resetPosition = function() {
      return this.change_value(this.options.default_value);
    };

    HearcloudPlayerUiSlider.prototype.startDrag = function(e) {
      var start_position,
        _this = this;
      e.preventDefault();
      start_position = $(this.container).offset();
      return $(document).bind('mousemove.HearcloudPlayerUiSlider', function(e) {
        var local_offset;
        local_offset = (e.pageX - start_position.left) / (_this.options.width - 0.5);
        return _this.change_value((_this.options.maximum - _this.options.minimum) * local_offset);
      }).bind('mouseup.HearcloudPlayerUiSlider', function() {
        return $(document).unbind('mousemove.HearcloudPlayerUiSlider mouseup.HearcloudPlayerUiSlider');
      });
    };

    HearcloudPlayerUiSlider.prototype.scroll = function(e) {
      if (e.originalEvent.wheelDelta > 0) {
        return this.change_value(this.value + 1);
      } else {
        return this.change_value(this.value - 1);
      }
    };

    HearcloudPlayerUiSlider.prototype.clear = function() {
      return this.graphic_context.clearRect(0, 0, this.container.width, this.container.height);
    };

    HearcloudPlayerUiSlider.prototype.draw = function() {
      var border, center, half_height, position;

      this.clear();
      center = Math.round(this.container.width / 2) + 0.5;
      half_height = Math.round(this.options.height / 2);

      // Draw track
      this.graphic_context.fillStyle = style.track_style;
      this.graphic_context.fillRect(0, half_height - 2.5, this.options.width, 4.5);
      // Draw shadow stroke
      this.graphic_context.beginPath();
      this.graphic_context.moveTo(0, half_height - 2.5);
      this.graphic_context.lineTo(this.options.width, half_height - 2.5);
      this.graphic_context.strokeStyle = 'rgba(0,0,0,0.3)';
      this.graphic_context.stroke();
      this.graphic_context.closePath();
      // Draw highlight stroke
      this.graphic_context.beginPath();
      this.graphic_context.moveTo(0, half_height + 2.5);
      this.graphic_context.lineTo(this.options.width, half_height + 2.5);
      this.graphic_context.strokeStyle = 'rgba(255,255,255,0.1)';
      this.graphic_context.stroke();
      this.graphic_context.closePath();
      // Draw center line
      this.graphic_context.beginPath();
      this.graphic_context.moveTo(center, 0);
      this.graphic_context.lineTo(center, this.options.height);
      this.graphic_context.strokeStyle = style.button_foreground;
      this.graphic_context.stroke();
      this.graphic_context.closePath();
      // Draw handle as 2 halfs
      this.graphic_context.fillStyle = style.button_background;
      position = ((this.value / (this.options.maximum - this.options.minimum)) * (this.options.width - 20)) + 0.5;
      this.graphic_context.fillRect(position, 0, 9.5, this.options.height);
      this.graphic_context.fillRect(position + 10.5, 0, 9.5, this.options.height);
      // Draw recticle on the handle
      this.graphic_context.beginPath();
      this.graphic_context.moveTo(position + 10, 0);
      this.graphic_context.lineTo(position + 10, this.options.height / 4);

      this.graphic_context.moveTo(position + 10, (this.options.height / 4) * 3);
      this.graphic_context.lineTo(position + 10, this.options.height);
      this.graphic_context.closePath();
      this.graphic_context.strokeStyle = style.button_foreground;
      this.graphic_context.stroke();

      border = this.graphic_context.createLinearGradient(0, 0, 0, this.container.height);
      border.addColorStop(0, 'rgba(255,255,255,0.2)');
      border.addColorStop(0.5, 'rgba(0,0,0,0.2)');
      this.graphic_context.beginPath();
      this.graphic_context.rect(position, 0.5, 20, this.options.height - 1);
      this.graphic_context.closePath();
      this.graphic_context.lineWidth = 1;
      this.graphic_context.strokeStyle = border;
      return this.graphic_context.stroke();
    };

    HearcloudPlayerUiSlider.prototype.change_value = function(new_value) {
      var proposed_value;
      // Clip value
      if (new_value > this.options.maximum) {
        new_value = this.options.maximum;
      }
      if (new_value < this.options.minimum) {
        new_value = this.options.minimum;
      }
      // Round value
      proposed_value = Math.round(new_value);
      // Only fire things up if value has changed
      if (proposed_value !== this.value) {
        this.value = proposed_value;
        this.draw();
        return this.options.on_change(this.value);
      }
    };

    return HearcloudPlayerUiSlider;
  })();
/* ************************************************************************* */
/* Colors style stuff */
  this.style = {
    track_style: '#333',
    button_background: '#333',
    button_active_background: '#666',
    button_alternate_background: '#555',
    button_foreground: '#ababab',
    button_active_foreground: '#F7F7F7',
    dial_foreground: '#222',
    dial_background: '#444',
    label_font: "normal 12px sans-serif",
    adjust: function(color, percent) {
      var B, BB, G, GG, R, RR;
      if (color.length === 4) {
        R = parseInt(color.substring(1, 2) + color.substring(1, 2), 16);
        G = parseInt(color.substring(2, 3) + color.substring(2, 3), 16);
        B = parseInt(color.substring(3, 4) + color.substring(3, 4), 16);
      } else {
        R = parseInt(color.substring(1, 3), 16);
        G = parseInt(color.substring(3, 5), 16);
        B = parseInt(color.substring(5, 7), 16);
      }
      R = parseInt(R * (100 + percent) / 100);
      G = parseInt(G * (100 + percent) / 100);
      B = parseInt(B * (100 + percent) / 100);

      R = R < 255 ? R : 255;
      G = G < 255 ? G : 255;
      B = B < 255 ? B : 255;

      RR = R.toString(16).length === 1 ? "0" + R.toString(16) : R.toString(16);
      GG = G.toString(16).length === 1 ? "0" + G.toString(16) : G.toString(16);
      BB = B.toString(16).length === 1 ? "0" + B.toString(16) : B.toString(16);
      return "#" + RR + GG + BB;
    }
  };
}).call(this);
